import pygame as pg

pg.init()

_display = pg.Surface((288,512))

screen = pg.display.set_mode((0,0))
sw, sh = screen.get_size()

image = pg.image.load("assets/sprites/game_images/background-day.png").convert()
_display.blit(image,(0,0))

while True:
	screen.fill("white")
	
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
	
	screen.blit(pg.transform.scale(_display, (sw, sh)), (0,0))
	
	pg.display.flip()