import pandas as pd
import re

class ParticipantResults:
	"Class for a given file of participant results on a video."

	VID_LIST_REGEX = re.compile('[\[\]\']')
	FOCUS_THRESHOLD = 75.0
	NUM_CHANGE_RATING_THRES = 3

	@classmethod
	def change_focus_threshold(cls, new_threshold):
		cls.FOCUS_THRESHOLD = new_threshold

	def __init__(self, video_name, orig_df, worker_info_df):
		self.video_name = video_name
		self.orig_df = orig_df
		self.modded_df = orig_df # SEE if we need a copy
		self.worker_info = worker_info_df
		self.average_df = pd.DataFrame()


	#################################################
	#					Cleaning					#
	#################################################

	def focusPercentageColumn(self, worker_id, video_name, row):

		"""
		Calculates whether video was the first, second, or third video watched by participant
		
		Args:
			self: class object
			worker_id: the string identifier of a participant
			video_name: video filename (w/ no file extention)
			row: a row in worker_info (given as pandas df)

		Returns:
			focusPercentageVid1, focusPercentageVid2, focusPercentageVid3, -1 if video was watched 
				first, second, third, or never watched, respectively.
		"""
		
		if row.empty:
			return -1 # worker might not be in worker_info?
		vid_list = re.sub(self.VID_LIST_REGEX, '', row['videoClips'].values[0]).split(', ') # list of vids participant watched

		for vid in vid_list:
			if video_name in vid:
				video_name = vid # see if we might want to change this??
				break
		return 'focusPercentageVid' + str(vid_list.index(video_name) + 1) if video_name in vid_list else -1


	def count_changes(self, row):
		"""
		Calculates the number of times a participant changed the value in the time series of the row

		Args:
			self: class object
			row: participant time series, pandas df

		Returns:
			True if participant changes value more than NUM_CHANGE_RATING_THRES times; False otherwise.
		"""

		count = currVal = -1

		# Skip the worker id in the first column
		for value in row.values[1:]:
			if currVal != value:
				count += 1
				currVal = value
			if count >= self.NUM_CHANGE_RATING_THRES:
				return True
		return False


	def clean(self, anim=True):
		"""
		Cleans the CSV file of participant data
	
		Args:
			self: class object
	
		Returns:
			Nothing explicitly - within the class object, it ends up with a modified dataframe.
		"""

		indicies = []

		for index, row in self.orig_df.iterrows():

			remove = False
			# return this stuff if the focusPercentageColumns come back -- I dont think they will


			# if anim == True:
			# 	worker_id = row['worker_id']
			# 	worker_row = self.worker_info.loc[self.worker_info['worker_id'] == worker_id]

			# 	# with a worker_id, we can cross_reference against worker_info
			# 	col_label = self.focusPercentageColumn(worker_id, self.video_name, worker_row)

			# 	# This is where we add the drops, etc
			# 	if col_label != -1:
			# 		percent_focus = worker_row[col_label].values[0]
			# 		if percent_focus < self.FOCUS_THRESHOLD:
			# 			remove = True
			# 		if self.count_changes(row) == False:
			# 			remove = True
			# 	else:
			# 		remove = True
			# else:
			if self.count_changes(row) == False:
				remove = True

			# ADD TO LIST
			if remove == True:
				indicies.append(index)


		print("Num people thrown out for video {}:".format(self.video_name), len(indicies), "out of {} participants".format(len(self.orig_df.index)))

		# MODIFY dataframe and reset row indicies
		if len(self.modded_df.index) != len(self.orig_df.index):
			return
		else:
			self.modded_df = self.modded_df.drop(indicies).reset_index(drop=True)


	#################################################
	#					Averaging					#
	#################################################


	def compute_average(self):
		"""
		Computes the average across all participants in the time frame given.

		Args:
			self: class object

		Returns:
			Nothing. Modifies average_df
		"""

		self.average_df = self.modded_df.mean(axis=0)
		#print(self.average_df)


	#################################################
	#					Correlating					#
	#################################################


	# leave for jupyter notebook - since it is over multiple objects (unless we want to create
	# some kind of built-in correlation? - this could also be pretty simple...)



