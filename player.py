import pygame as pg
import random
import config

def load(image_name):
	img = pg.image.load(f"assets/sprites/bird/{image_name}").convert_alpha()
	fx, fy = 6,6
	iw, ih = config.scale.scaler(fx,fy,img.get_size())
	img = pg.transform.scale(img, (iw,ih))
	return img

class Player(pg.sprite.Sprite):
	
	def __init__(self, x, y, factor_y, base_y):
		super().__init__()
		
		# Bird Images
		self.images = {
		
		"red": {
			0: load("redbird-downflap.png"),
			1: load("redbird-midflap.png"),
			2: load("redbird-upflap.png")
			},
			
		"blue": {
			0: load("bluebird-downflap.png"),
			1: load("bluebird-midflap.png"),
			2: load("bluebird-upflap.png")
			},
			
		"yellow": {
			0: load("yellowbird-downflap.png"),
			1: load("yellowbird-midflap.png"),
			2: load("yellowbird-upflap.png")
			}
		}
		
		# Bird color
		image_choices = ["red","blue","yellow"]
		self.bird_color = random.choice(image_choices)
		
		# Frame Mechanics
		self.current_frame = 0
		self.frame_counter = 0
		self.max_frame = 12
		
		# Image and Rect
		self.pos = (x,y)
		self.image = self.images[self.bird_color][self.current_frame]
		self.rect = self.image.get_rect(center=self.pos)
		
		# Sounds
		self.hit = pg.mixer.Sound("assets/audio/hit.ogg")
		self.die = pg.mixer.Sound("assets/audio/die.ogg")
		self.point = pg.mixer.Sound("assets/audio/point.ogg")
		self.wing = pg.mixer.Sound("assets/audio/wing.ogg")
		
		# Velocity
		self.vel = 0
		
		# Bird Stats
		self.alive = True
		self.flap = False
		self.touching_ground = False
		self.doanimate = True
		self.score = 0
		self.collided = False
		
		# Rotated Image
		self.rotated_img = None
		
		# Factors
		self.factor_y = factor_y # Only need factorY since movement is in y-axis only
		self.ground = base_y
			
	def animate(self):
		
		if self.alive:
			self.frame_counter += 1
			if self.frame_counter >= self.max_frame:
				self.current_frame += 1
				if self.current_frame > 2:
					self.current_frame = 0
				self.frame_counter = 0
		
		self.image = self.images[self.bird_color][self.current_frame]
		self.rotated_img = pg.transform.rotate(self.image, self.vel * -2)
	
	def update(self):
		if self.rect.bottom < self.ground:
			self.vel += 0.5 * self.factor_y
			
			if self.flap:
				self.vel = -12 * self.factor_y
				self.wing.play()
				self.flap = False
			
			self.rect.y += self.vel
		
		else:
			self.touching_ground = True
			self.doanimate = False
			self.alive = False
	
	def update_score(self):
		self.score += 1
		self.point.play()
	
	def reset(self, player_pos):
		self.alive = True
		self.touching_ground = False
		self.rotated_img = None
		self.current_frame = 0
		self.frame_counter = 0
		self.doanimate = True
		self.vel = 0
		self.score = 0
		self.rect.center = player_pos
		image_choices = ["red","blue","yellow"]
		self.bird_color = random.choice(image_choices)
		
	def draw(self, display):
		if self.doanimate:
			self.animate()
			
		display.blit(self.rotated_img, self.rect)
		#pg.draw.rect(display, rect=self.rect, color="red", width=2)