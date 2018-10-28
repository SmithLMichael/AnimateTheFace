# Filename: Of_CSVtoCSV.py
# Author: Michael L. Smith
#
# Takes in a directory of CSVs generated from OpenFace 2.0 FeatureExtractor's function and
# converts them to the necessary format needed for my animations.

import os
import numpy as np
import pandas as pd
from toolz import interleave


directory = os.fsencode('/Users/MichaelSmith/Desktop/CSVs/OF_CSVs')

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	savename = filename[:10]

	print(filename)
	if '.csv' in filename:
		#print(filename)
		csv_pd = pd.read_csv(os.path.join(os.fsdecode(directory), filename))
		X = csv_pd.loc[:, ' x_0':' x_67']
		Y = csv_pd.loc[:, ' y_0':' y_67']
		XY = pd.DataFrame(interleave([X.values, Y.values])).T
		XY.to_csv('/Users/MichaelSmith/Desktop/CSVs/ANIM_CSVs/' + savename + '.csv', index=False, header=False)


