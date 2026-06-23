import pygame as pg
import config
import random
import os

def load_img(path):
	fx, fy = 6,6
	base_path = os.path.dirname(os.path.abspath(__file__))
	img_path = os.path.join(base_path, f"assets/sprites/game_images/{path}") 
	img = pg.image.load(img_path)
	img = pg.transform.scale(img, config.scale.scaler(fx,fy,img.get_size()))
	
	return img
	
class ScrollingLayer(pg.sprite.Sprite):
	
	def __init__(self, pathA, x, y, dx, pathB=None, background=False):
		self.display = pg.display.get_surface()
		self.screen_width = self.display.get_width()
		
		if not background:
			# Handles Base
			self.image = load_img(pathA).convert_alpha()
			self.image2 = self.image.copy()
		else:
			self.imageA = load_img(pathA).convert()
			self.imageB = load_img(pathB).convert()
			
			self.image = random.choice([self.imageA, self.imageB])
			self.image2 = self.image.copy()
			self.frame_counter = 0
			self.max_frame = 12 # Update every 12 frames
			
		
		# Common variables
		self.dx = dx * config.scale.factor_x
		
		topleft_rect = (x,y)
		topleft_rect2 = (self.screen_width,y)
		self.rect = self.image.get_rect(topleft=topleft_rect)
		self.rect2 = self.image2.get_rect(topleft=topleft_rect2)
		
		self.background = background
	
	def update(self):
		self.rect.x -= self.dx 
		self.rect2.x -= self.dx 
			
		if self.rect.right <= 0:
			self.rect.left = self.rect2.x + self.image.get_width()
		if self.rect2.right <= 0:
			self.rect2.left = self.rect.x + self.image2.get_width()
	
	def change_background(self):
		self.image = random.choice([self.imageA, self.imageB])
		self.image2 = self.image.copy()
	
	def draw(self):
		render = [(self.image, self.rect), (self.image2, self.rect2)]
		self.display.blits(render)