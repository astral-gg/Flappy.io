import pygame as pg
import config
import os
import json
from datetime import datetime

def load_img(fx,fy,path):
	fx, fy = fx,fy
	base_path = os.path.dirname(os.path.abspath(__file__))
	img_path = os.path.join(base_path, f"assets/sprites/score_board/{path}")
	img = pg.image.load(img_path).convert_alpha()
	img = pg.transform.scale(img, config.scale.scaler(fx,fy,img.get_size()))
	return img

def create_boards(score, images):
	digits = [int(n) for n in str(score)]
	
	score_board = pg.Surface((images[0].get_width() * (len(digits) + 1), images[0].get_height())).convert()
	score_board.set_colorkey((0,0,0))
	   
	for idx in range(len(digits)):
		num_img = images[int(digits[idx])]
		y = score_board.get_height()//2
		
		if digits[idx] != 1:
		      x = num_img.get_width()//2 + num_img.get_width() * idx
		else:
		      width = num_img.get_width() + (images[0].get_width() - num_img.get_width())
		      x = width * idx + width//2
	       
		num_rect = num_img.get_rect()
		num_rect.center = (x, y)
	       
		score_board.blit(num_img, num_rect)

	return score_board

class Score():
	"""
	Score class is used to track the player's
	score(live) and display it.
	It is also used to display the score board
	at the end of current game!
	"""
	def __init__(self, player, x, y):
		# Get Display surface
		self.display = pg.display.get_surface()
		self.screen_width, self.screen_height = self.display.get_size()
		
		# Numbers
		nfx, nfy = 5,5
		self.numbers = []
		for n in range(0,10):
			self.numbers.append(load_img(nfx,nfy,f"numbers/{n}.png"))
		
		# ScoreBoard - Numbers
		nfx, nfy = 1,1
		self.digits = []
		for n in range(0,10):
			self.digits.append(load_img(nfx,nfy,f"numbers/{n}.png"))
			
		# Player
		self.player = player
		
		# Medals
		# ===================
		# UNCOMMENT AFTER ADDING MEDALS AND BOARD
		# ===================
		mfx,mfy = 9,9
		self.gold = load_img(mfx,mfy,"gold_medal.png")
		self.silver = load_img(mfx,mfy,"medal.png")
		#self.tin = load_img(mfx,mfy,"tin.png")
#		self.bronze = load_img(mfx,mfy,"bronze.png")
		
		# Score Board
		self.score_board = load_img(mfx,mfy,"score_board.png")
		self.score_board_rect = self.score_board.get_rect(center=(x,y))
		
		# Trying adjustments
		self._cached_score = None
		self._cached_board = None
		
		# These for the ondeath board
		self._board_key = None
		self._board_cache = None
	
	def _build_board(self, current_score, best_score):
	   current_display = create_boards(current_score, self.digits)
	   current_rect = current_display.get_rect(center=(self.score_board.get_width() * 0.8, self.score_board.get_height() * 0.35))
	   
	   best_display = create_boards(best_score, self.digits)
	   best_rect = best_display.get_rect(center=(self.score_board.get_width() * 0.8, self.score_board.get_height() * 0.7))
	   
	   medal_rect = self.gold.get_rect()
	   medal_rect.centery = self.score_board.get_height() * 0.53
	   medal_rect.centerx = self.score_board.get_height() * 0.42
	   
	   new_board = pg.Surface(self.score_board.get_size()).convert()
	   new_board.fill((0,0,0))
	   new_board.blit(self.score_board, (0,0))
	   new_board.blit(self.gold if current_score > best_score else self.silver, medal_rect)
	   new_board.blit(current_display, current_rect)
	   new_board.blit(best_display, best_rect)
	   new_board.set_colorkey((0,0,0))
	   return new_board
	
	def draw_score_board(self, prev_score):
	   	current_score = self.player.score
	   	key = (current_score, prev_score)
	   	
	   	if key != self._board_key:
	   		self._board_key = key
	   		self._board_cache = self._build_board(current_score, prev_score)
	   		if current_score > prev_score:
	   			self.save_score()
	   	
	   	self.display.blit(self._board_cache, self.score_board_rect)


	
	#def draw_score_board(self, prev_score):
#		# Retrieve Scores
#		current_score = self.player.score
#		best_score = prev_score
#		
#		# Make score display
#		current_score_display = create_boards(current_score, self.digits)
#		current_score_display_rect = current_score_display.get_rect()
#		current_score_display_rect.center = (self.score_board.get_width() * 0.8, self.score_board.get_height() * 0.35)
#		
#		best_score_display = create_boards(best_score, self.digits)
#		best_score_display_rect = best_score_display.get_rect()
#		best_score_display_rect.center = (self.score_board.get_width() * 0.8, self.score_board.get_height() * 0.7)
#		
#		medal_rect = self.gold.get_rect()
#		new_board = self.score_board.copy()
#		
#		medal_rect.centery = new_board.get_height() * 0.53
#		medal_rect.centerx = new_board.get_height() * 0.42
#		
#		# Blit on new_board
#		if current_score > best_score:
#			new_board.blit(self.gold, medal_rect)
#		else:
#			new_board.blit(self.silver, medal_rect)
#		
#		new_board.blit(current_score_display, current_score_display_rect)
#		new_board.blit(best_score_display, best_score_display_rect)
#			
#		self.display.blit(new_board, self.score_board_rect)
#		
#		if current_score > best_score:
#			self.save_score()
#	
	def show_score(self):
		if self._cached_score != self.player.score:
			self._cached_score = self.player.score
			self._cached_board = create_boards(self._cached_score, self.numbers)
			self._cached_rect = self._cached_board.get_rect()
			self._cached_rect.center = (self._cached_board.get_width()//8 + self.screen_width * 0.5, self.screen_height * 0.15)
		
		self.display.blit(self._cached_board, self._cached_rect)
		
	def save_score(self):
		with open("score.txt","w") as f:
			f.write(f"{self.player.score}")
	
	def load_score(self):
		with open("score.txt","r") as f:
			score = f.read()
			return int(score)
	
	def log_statistics(self, death_cause, number_of_clicks, bird_max_height, bird_min_height, runtime, version):
		timestamp = datetime.timestamp(datetime.now())
		
		if death_cause == None:
			death_cause = "Collided with Ground"
			
		entry = {
			
			"Version": version,
			"Timestamp": timestamp,
			"Score": self.player.score,
			"Cause of Death": death_cause,
			"Number of Flaps": number_of_clicks,
			"Bird max Height": bird_max_height,
			"Bird min Height": bird_min_height,
			"Run Time": runtime
		}
		
		try:
			with open("stats.json","r") as file:
				data = json.load(file)
		except FileNotFoundError:
			data = []
		
		data.append(entry)
		
		with open("stats.json","w") as file:
			json.dump(data,file)