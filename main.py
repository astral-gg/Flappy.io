import pygame as pg
from utils import Scaler
import config
import sys
import os

# Game Related Imports 
from player import Player
from pipes import Pipes
from scrollinglayer import ScrollingLayer
from score import Score

os.environ["PYGAME_BLEND_ALPHA_SDL2"] = "1"

pg.init()

class Game():
	
	def __init__(self):
		self.display = pg.display.set_mode()
		self.width, self.height = self.display.get_size()
		self.clock = pg.time.Clock()
		
		self.global_start_time = pg.time.get_ticks()
		
		config.scale = Scaler((self.width, self.height))
		
		# Game state
		self.pause = False
		
		# Movement Speed for Base and Pipes
		self.pipe_base_dx = 5
		
		# Base
		self.base = ScrollingLayer("base.png", 0, self.height*0.80, dx=self.pipe_base_dx)
		
		# Player
		self.player_pos = (int(self.width * 0.12), int(self.height//2))
		self.player = Player(self.player_pos[0], self.player_pos[1], config.scale.factor_y, self.base.rect.y)
	
	def level(self):
		# Background
		background = ScrollingLayer(pathA="background-day.png", pathB="background-night.png",x=0,y=-self.height*0.1,dx=1,background=True)
		
		# Pipe Group
		pipe_gap = self.player.image.get_height() * 3
		pipe_delay = 2300
		last_pipe_spawn = 0
		pipe_group = pg.sprite.Group()
		pipes = Pipes(pipe_gap, self.base.rect.y, self.player, self.pipe_base_dx)
		
		# Game Loop
		while True:
			self.display.fill((0,0,0))
			self.clock.tick(config.fps)
			background.draw()
			
			# Pipes
			if pg.time.get_ticks() - last_pipe_spawn > pipe_delay:
				pipes.generate_pipe(pipe_group, pipe_gap, self.base.rect.y, self.player, self.pipe_base_dx, pipes)
				last_pipe_spawn = pg.time.get_ticks()
			
			elif len(pipe_group) == 0:
				pipes.generate_pipe(pipe_group, pipe_gap, self.base.rect.y, self.player, self.pipe_base_dx, pipes)
				last_pipe_spawn = pg.time.get_ticks()
			
			# Update — Only if player is alive
			if self.player.alive:
				pipe_group.update()
				self.base.update()
				background.update()
			
			if pipe_group and self.player.alive:
				for pipe in pipe_group:
					if self.player.rect.colliderect(pipe.inverted_rect):
						self.player.alive = False
						self.player.hit.play()
						self.player.die.play()
						pg.draw.rect(self.display, rect=pipe.inverted_rect, color="red")
						
					if self.player.rect.colliderect(pipe.normal_rect):
						self.player.alive = False
						self.player.hit.play()
						self.player.die.play()
						pg.draw.rect(self.display, rect=pipe.normal_rect, color="red")
					
					if self.player.rect.left > pipe.gap_surface_rect.right and not pipe.awarded:
						pipe.awarded = True
						self.player.update_score()
			
			if self.player.rect.y < -self.player.image.get_height():
				self.player.alive = False
			
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					sys.exit()
					
				if event.type == pg.FINGERDOWN and self.player.alive:
					self.player.flap = True
				
				if event.type == pg.FINGERDOWN and self.player.touching_ground:
					print(self.player.score)
					pipe_group.empty()
					self.player.reset(self.player_pos)
					Pipes.pipe_count = 0
					background = ScrollingLayer(pathA="background-day.png", pathB="background-night.png",x=0,y=-self.height*0.1,dx=1,background=True)
				
			# Draw Logic
			pipe_group.draw(self.display)
			self.player.update()
			self.player.draw(self.display)
			self.base.draw()
			
			pg.display.flip()

if __name__ == "__main__":
	game = Game()
	game.level()