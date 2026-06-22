import pygame as pg
import config
import os

def load_img(fx,fy,path):
	fx, fy = fx,fy
	base_path = os.path.dirname(os.path.abspath(__file__))
	img_path = os.path.join(base_path, f"assets/sprites/score_board/{path}")
	img = pg.image.load(img_path).convert_alpha()
	img = pg.transform.scale(img, config.scale.scaler(fx,fy,img.get_size()))
	return img

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
		nfx, nfy = 1,1
		numbers = {}
		for n in range(0,10):
			numbers[f"{n}"] = load_img(nfx,nfy,f"numbers/{n}.png")
			
		# Player
		self.player = player
		
		# Medals
		# ===================
		# UNCOMMENT AFTER ADDING MEDALS AND BOARD
		# ===================
		#mfx,mfy = 7,7
#		self.gold = load_img(mfx,mfy,"gold.png")
#		self.silver = load_img(mfx,mfy,"silver.png")
#		self.tin = load_img(mfx,mfy,"tin.png")
#		self.bronze = load_img(mfx,mfy,"bronze.png")
#		
#		# Score Board
#		self.score_board = load_img(7,7,"score_board.png")
#		self.score_board_rect = self.score_board.get_rect(center=(x,y))
	
	#def draw_score_board(self):
#		medal_rect = self.gold.get_rect()
#		new_board = self.score_board.copy()
#		
#		medal_rect.centery = new_board.get_height() * 0.55
#		medal_rect.centerx = new_board.get_height() * 0.45
#		
#		new_board.blit(self.gold, medal_rect)
#		self.display.blit(new_board, self.score_board_rect)
	
	def show_score(self):
		player_score = f"{self.player.score}"
		