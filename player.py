import pygame as pg
import random
import config
import os

def load(image_name):
	base_path = os.path.dirname(os.path.abspath(__file__))
	img_path = os.path.join(base_path, f"assets/sprites/bird/{image_name}")
	img = pg.image.load(img_path).convert_alpha()
	fx, fy = 6,6
	iw, ih = config.scale.scaler(fx,fy,img.get_size())
	img = pg.transform.scale(img, (iw,ih))
	return img

TILT_STEP = 2
TILT_MIN = -90
TILT_MAX = 45

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
		self.rect.width = self.rect.width - 35
		
		# Sounds
		base_path = os.path.dirname(os.path.abspath(__file__))
		self.hit = pg.mixer.Sound(os.path.join(base_path, "assets/audio/hit.ogg"))
		self.die = pg.mixer.Sound(os.path.join(base_path, "assets/audio/die.ogg"))
		self.point = pg.mixer.Sound(os.path.join(base_path, "assets/audio/point.ogg"))
		self.point.set_volume(0.025)
		self.wing = pg.mixer.Sound(os.path.join(base_path, "assets/audio/wing.ogg"))
		self.wing.set_volume(0.10)
		
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
		self._rotated_img = {}
		
		#for color, frames in self.images.items():
#			for frame, img in frames.items():
#				for angle in range(TILT_MIN, TILT_MAX+1, TILT_STEP):
#					self._rotated_img[(color, frame, angle)] = pg.transform.rotate(img, angle)
#		
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
		
		#angle = round((self.vel * -2)/TILT_STEP) * TILT_STEP
#		angle = max(TILT_MIN, min(TILT_MAX, angle))
#		self.rotated_img = self._rotated_img[(self.bird_color, self.current_frame, angle)]
#		
		self.rotated_img = self.image
		
	def update(self):
		if self.rect.bottom < self.ground:
			#self.vel += 0.98 * self.factor_y
			self.vel += 1.15 * self.factor_y
			
			if self.flap:
				self.vel = -18 * self.factor_y
				self.vel = -21.8 * self.factor_y
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
			
		display.blit(self.rotated_img, self.rotated_img.get_rect(center=self.rect.center))
		#pg.draw.rect(display, rect=self.rect, color="red", width=2)