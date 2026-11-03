import json
from datetime import datetime

class Statistics():
	
	def __init__(self, file_name):
		try:
			with open(file_name,"r") as file:
				self.data = json.load(file)
		except FileNotFoundError:
			self.data = []
		
		if self.data != []:
			self.play_dates = set(datetime.fromtimestamp(_).strftime("%Y-%b-%d") for _ in sorted(self.get_data_field("Timestamp")))
			self.games_played = len(self.data)
			
			self.total_play_time = sum(self.get_data_field("Run Time"))
			self.highest_score = max(self.get_data_field("Score"))
			self.lowest_score = min(self.get_data_field("Score"))
			
			self.average_score = sum(self.get_data_field("Score"))/self.games_played
			
	def get_data_field(self, target_data_field):
		return [self.data[idx][target_data_field] for idx in range(len(self.data))]
	
	def score_avg(self):
		scores = sum(self.get_data_field("Score"))
		return scores/self.games_played