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

#os.environ["PYGAME_BLEND_ALPHA_SDL2"] = "1"

pg.init()

font = pg.font.Font(None, 43)
def show_info(text, pos, screen):
	_txt_surface = font.render(f"FPS: {text}", True, "white")
	screen.blit(_txt_surface, pos)

class Game():
	
	def __init__(self):
		
		# Version - Changes after major updates
		self.version = 1.1
		
		self.display = pg.display.set_mode((0,0), pg.FULLSCREEN)
		self.width, self.height = self.display.get_size()
		self.clock = pg.time.Clock()
		
		self.global_start_time = pg.time.get_ticks()
		
		config.scale = Scaler((self.width, self.height))
		
		# Game state
		self.pause = False
		
		# Movement Speed for Base and Pipes
		#self.pipe_base_dx = 915
		self.pipe_base_dx = 12
		
		# Base
		self.base = ScrollingLayer("base.png", 0, self.height*0.80, dx=self.pipe_base_dx)
		
		# Player
		self.player_pos = (int(self.width * 0.12), int(self.height//2))
		self.player = Player(self.player_pos[0], self.player_pos[1], config.scale.factor_y, self.base.rect.y)
		
		# Game State Variables
		self.start = False
		self.pause = False
		self.log_stats = True # Dont set true theres a bug in pipe generation. FIX IT!
		
		# Score
		self.score = Score(self.player, self.width * 0.5, self.height * 0.6)
	
	def level(self):
		# Background
		background = ScrollingLayer(pathA="background-day.png", pathB="background-night.png",x=0,y=-self.height*0.28,dx=1,background=True)
		
		# Pipe Group
		pipe_gap = self.player.image.get_height() * 4
		#pipe_spawn_delay = 950
		pipe_spawn_delay = 1150
		
		last_pipe_spawn = 0
		pipe_group = pg.sprite.Group()
		pipes = Pipes(pipe_gap, self.base.rect.y, self.player, self.pipe_base_dx, None)
		last_pipe_spawn = pg.time.get_ticks()
		
		# Stats
		number_of_clicks = 0
		death_cause = None
		max_y = min_y = self.player.rect.y
		
		# Score
		try:
			prev_score = self.score.load_score()
		except FileNotFoundError:
			prev_score = 0
		
		last_score = 0
		
		# Game Loop
		while True:
			#pipe_spawn_delay = (self.width / self.pipe_base_dx) * pipe_spawn_control_factor
			self.display.fill((0,0,0))
			self.clock.tick(config.fps)
			background.draw()
			
			# Pipes Spawn
			# Spawn pipes only if game has started
			if self.start and self.player.alive:
				
				if len(pipe_group) != 0:
					last_pipe_gap_pos = pipe_group.sprites()[-1].y
				else:
					last_pipe_gap_pos = None
					
				if pg.time.get_ticks() - last_pipe_spawn > pipe_spawn_delay:
					pipes.generate_pipe(pipe_group, pipe_gap, self.base.rect.y, self.player, self.pipe_base_dx, pipes, last_pipe_gap_pos)
					last_pipe_spawn = pg.time.get_ticks()
				
				elif len(pipe_group) == 0:
					pipes.generate_pipe(pipe_group, pipe_gap, self.base.rect.y, self.player, self.pipe_base_dx, pipes, last_pipe_gap_pos)
					last_pipe_spawn = pg.time.get_ticks()
				
			# Update Player — If game has started
			if self.start:
				self.player.update()
			
			# Update — Only if player is alive
			if self.player.alive:
				pipe_group.update()
				self.base.update()
				background.update()
				
				# Heights with respect to base
				max_y = max(max_y, self.base.rect.y - self.player.rect.y)
				min_y = min(min_y, self.base.rect.y - self.player.rect.y)
			
			# Collision Detection Logic
			if pipe_group and self.player.alive:
				for pipe in pipe_group:
					if self.player.rect.colliderect(pipe.inverted_rect):
						death_cause = "Collided with Inverted pipe"
						self.player.hit.play()
						self.player.die.play()
						pg.draw.rect(self.display, rect=pipe.inverted_rect, color="red")
						self.player.alive = False
						self.player.vel -= 9
						
					if self.player.rect.colliderect(pipe.normal_rect):
						death_cause = "Collided with Normal Pipe"
						self.player.hit.play()
						self.player.die.play()
						pg.draw.rect(self.display, rect=pipe.normal_rect, color="red")
						self.player.alive = False
						self.player.vel -= 9
					
					if self.player.rect.left > pipe.gap_surface_rect.right and not pipe.awarded:
						pipe.awarded = True
						self.player.update_score()
			
			if self.player.rect.y < -self.player.image.get_height():
				death_cause = "Flew out of screen"
				self.player.alive = False
			
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					sys.exit()
				
				#if event.type == pg.FINGERDOWN:
#					if event.y * self.height < self.height // 2 :
#						self.pause = not self.pause
				
				if (event.type == pg.FINGERDOWN or event.type == pg.KEYDOWN) and self.start == False:
					self.start = True
					self.global_start_time = pg.time.get_ticks()
					
				if (event.type == pg.FINGERDOWN or event.type == pg.KEYDOWN) and self.player.alive:
					self.player.flap = True
					number_of_clicks += 1
				
				if (event.type == pg.FINGERDOWN or event.type == pg.KEYDOWN) and self.player.touching_ground:
					self.display.fill("black")
					pipe_group.empty()
					Pipes.pipe_count = 0
					background.change_background()
					self.start = False
					
					# Log stats
					if self.log_stats:
						self.score.log_statistics(death_cause, number_of_clicks-1, max_y, min_y, pg.time.get_ticks() - self.global_start_time, self.version)
					
					# Reset Stats & Player variables
					number_of_clicks = 0
					death_cause = None
					self.player.reset(self.player_pos)
					max_y = min_y = self.player.rect.y
					
					try:
						prev_score = self.score.load_score()
					except FileNotFoundError:
						prev_score = 0
					
			# Draw Logic
			pipe_group.draw(self.display)
			self.player.draw(self.display)
			self.base.draw()
			show_info(self.clock.get_fps(), (0,0), self.display)
			if self.player.score != last_score:
				self.score.show_score()
				
			if not self.player.alive:
				self.score.draw_score_board(prev_score)
			
			if self.pause:
				continue
			
			pg.display.flip()

if __name__ == "__main__":
	game = Game()
	game.level()