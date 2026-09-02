import pygame as pg
import random
import config
import os

def load_img(path):
	pfx, pfy = 6,6
	base_path = os.path.dirname(os.path.abspath(__file__))
	img_path = os.path.join(base_path, f"assets/sprites/game_images/{path}")
	img = pg.image.load(img_path).convert_alpha()
	img = pg.transform.scale(img, config.scale.scaler(pfx,pfy,img.get_size()))
	return img

class Pipes(pg.sprite.Sprite):
	
	# Pipe Counts
	pipe_count = 0
	
	_green_pipe = None
	_green_pipe_inverted = None
	_red_pipe = None
	_red_pipe_inverted = None
	
	@classmethod
	def _cache_images(cls):
		if cls._green_pipe is None:
			cls._green_pipe = load_img("pipe-green.png")
			cls._green_pipe_inverted = pg.transform.flip(cls._green_pipe.copy(), False, True)
			
			cls._red_pipe = load_img("pipe-red.png")
			cls._red_pipe_inverted = pg.transform.flip(cls._red_pipe.copy(), False, True)
	
	def __init__(self, pipe_gap, ground, player, dx, last_pipe_gap_pos):
		super().__init__()
		
		Pipes._cache_images()
		
		# Get Display
		self.display = pg.display.get_surface()
		self.screen_width, self.screen_height = self.display.get_size()
		
		# Load pipes
		self.green_pipe = Pipes._green_pipe
		self.green_pipe_inverted = Pipes._green_pipe_inverted
		self.red_pipe = Pipes._red_pipe
		self.red_pipe_inverted = Pipes._red_pipe_inverted
		
		# Creating the Master-Surface
		self.surface = pg.Surface((self.green_pipe.get_width(),ground))
		#self.surface.fill((0,0,0))
		self.surface.set_colorkey((0,0,0))
		self.surface_rect = self.surface.get_rect(topleft=(self.screen_width,0))
		
		# Creating Gap-surface
		self.gap_surface = pg.Surface((self.green_pipe.get_width(),pipe_gap)).convert()
		self.gap_surface.fill("white")
		self.gap_surface.set_colorkey("white")
		
		if last_pipe_gap_pos == None:
			self.y = random.randint(0, self.surface.get_height()-pipe_gap)
		else:
			new_pipe_pos = random.randint(last_pipe_gap_pos - pipe_gap, last_pipe_gap_pos + pipe_gap)
			
			if new_pipe_pos > self.surface.get_height()-pipe_gap:
				new_pipe_pos = last_pipe_gap_pos - pipe_gap - random.randint(100,150)
			
			if new_pipe_pos < 0:
				new_pipe_pos = last_pipe_gap_pos + pipe_gap + random.randint(100,150)
				
			self.y = new_pipe_pos
			
		self.gap_surface_rect = self.gap_surface.get_rect(topleft=(0,self.y))
		
		self.surface.blit(self.gap_surface, self.gap_surface_rect)
		
		# Drawing pipe with respect to gap surface
		inverted_pipe_pos = (0, self.gap_surface_rect.y - self.green_pipe_inverted.get_height())
		normal_pipe_pos = (0, self.gap_surface_rect.y + pipe_gap)
		
		
		self.inverted_rect = self.red_pipe_inverted.get_rect(topleft=(inverted_pipe_pos))
		self.normal_rect = self.red_pipe.get_rect(topleft=(normal_pipe_pos))
		
		if (self.pipe_count+1)%10 == 0:
			self.surface.blit(self.red_pipe_inverted, self.inverted_rect)
			self.surface.blit(self.red_pipe, self.normal_rect)
		else:
			self.surface.blit(self.green_pipe_inverted, self.inverted_rect)
			self.surface.blit(self.green_pipe, self.normal_rect)
		
		# Movement Speed
		self.dx = dx * config.scale.factor_x
		
		self.image = self.surface.convert()
		self.rect = self.surface_rect
		
		self.awarded = False
	
	def update(self):
		self.surface_rect.x -= self.dx
		self.inverted_rect.x = self.surface_rect.x
		self.normal_rect.x = self.surface_rect.x
		self.gap_surface_rect.x = self.surface_rect.x
		
		if self.surface_rect.x <= -(self.surface.get_width()):
			self.kill()
	
	def add_pipe(self):
		Pipes.pipe_count += 1
			
	@staticmethod
	def generate_pipe(pipe_group, pipe_gap, ground, player, dx, pipe_instance, last_pipe_gap_pos):
		pipe_instance.add_pipe()
		pipe_group.add(Pipes(pipe_gap, ground, player, dx, last_pipe_gap_pos))