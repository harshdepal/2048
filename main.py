import pygame,sys,random,pickle
from pygame.locals import *
from classes import Field

try:
	with open('highscore.dat','rb') as file:
		highscore = pickle.load(file)
except:
	highscore = 0
pygame.init()
width , height = 700,700
topx , topy = 100,150
last = pygame.time.get_ticks()
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("2048")


field = Field()
field.highscore = highscore
while (True):
	current = pygame.time.get_ticks()
	if (field.moveMade and not field.gameOver):
		field.generateTile()
		field.moveMade = False
	field.display(window,topx,topy)
	for event in pygame.event.get():
		if (event.type == QUIT):
			with open('highscore.dat','wb') as file:
				pickle.dump(highscore,file)
			pygame.quit()
			sys.exit()
		elif (event.type == pygame.KEYDOWN and not field.gameOver):
			if (event.key == pygame.K_UP):
				field.moveTiles(0,-1)
			elif (event.key == pygame.K_DOWN):
				field.moveTiles(0,1)
			elif (event.key == pygame.K_LEFT):
				field.moveTiles(-1,0)
			elif (event.key == pygame.K_RIGHT):
				field.moveTiles(1,0)
	if (pygame.mouse.get_pressed()[0]==True and current-last > 1000):
		if (field.checkNewGame()):
			field = Field()
			last = pygame.time.get_ticks()
	field.checkGameOver()
	pygame.display.update()