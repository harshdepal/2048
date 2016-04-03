import pygame,sys,random
from pygame.locals import *

class Block:

	def __init__(self):
		self.value = 0

	def display(self,window,topx,topy):
		tileSize , textSize , textColor = 106.25 , 80 , (119,110,101)
		tileColor = {0:(187,173,160),2:(238,228,218),4:(237,224,200),8:(242,177,121),16:(245,149,99),32:(246,124,95),64:(246,94,59),128:(237,204,97),256:(237,204,97),512:(237,200,80),1024:(237,197,63),2048:(237,194,46)}
		pygame.draw.rect(window,tileColor[self.value],(topx,topy,tileSize,tileSize))
		if (self.value >= 128 and self.value < 1024):
			textSize = 70
		elif (self.value >= 1024 and self.value <= 2048):
			textSize = 60
		if (self.value > 8):
			textColor = (249,246,242)
		if (self.value == 0):
			return
		myFont = pygame.font.Font(None,textSize)
		myFont.set_bold(True)
		number = myFont.render(str(self.value),True,textColor,tileColor[self.value])
		numbRect = number.get_rect()
		numbRect.center = (topx + tileSize/2,topy + tileSize/2)
		window.blit(number,numbRect)

class Field:

	def __init__(self):

		self.__block = []
		for x in range (4):
			self.__block.append([])
			for y in range (4):
				self.__block[x].append(Block())
		self.generateTile()
		self.moveMade = True
		self.__score = 0
		self.highscore = 0
		self.gameOver = False
		self.message = "2048"

	def display(self,window,topx,topy):

		gridSize,tileSize,tileMargin,gridColor,WHITE = 500,106.25,15,(159,129,112),(255,255,255)
		window.fill(WHITE)
		pygame.draw.rect(window,gridColor,(topx,topy,gridSize,gridSize))
		for i in range (4):
			for j in range (4):
				self.__block[i][j].display(window,topx+tileMargin+i*(tileMargin+tileSize),topy+tileMargin+j*(tileMargin+tileSize))
		
		headColor,htopx,htopy = (119,110,101),50,25
		myFont = pygame.font.Font(None,90)
		head2048 = myFont.render(self.message,True,headColor,WHITE)
		headRect = head2048.get_rect()
		headRect.topleft = (htopx,htopy)
		window.blit(head2048,headRect)

		bgColor,tscoreColor,stopx,stopy = (187,173,160),(249,246,242),375,25
		scoreFont = pygame.font.Font(None,24)
		scoreText = scoreFont.render(str(self.__score),True,WHITE,bgColor)
		tscoreFont = pygame.font.Font(None,24)
		tscoreText = tscoreFont.render("SCORE",True,tscoreColor,bgColor)
		twidth,theight = tscoreFont.size("SCORE")
		swidth,sheight = scoreFont.size(str(self.__score))
		width,height = max(twidth,swidth) , theight + sheight
		tscoreRect = tscoreText.get_rect()
		tscoreRect.topleft = (stopx+width/2-twidth/2+5,stopy+5)
		scoreRect = scoreText.get_rect()
		scoreRect.topleft = (stopx+width/2-swidth/2+5,stopy+theight+5)
		pygame.draw.rect(window,bgColor,(stopx,stopy,width+10,height+10))
		window.blit(scoreText,scoreRect)
		window.blit(tscoreText,tscoreRect)

		bstx,bsty = 475,25
		bestText = scoreFont.render(str(self.highscore),True,WHITE,bgColor)
		bestRect = bestText.get_rect()
		bwidth,bheight = scoreFont.size(str(self.highscore))
		tbstText = tscoreFont.render("BEST",True,tscoreColor,bgColor)
		tbstRect = tbstText.get_rect()
		tbwidth,tbheight = tscoreFont.size("BEST")
		mwidth,mheight = (max(bwidth,tbwidth),bheight+tbheight)
		tbstRect.topleft = (bstx+mwidth/2-tbwidth/2+5,bsty+5)
		bestRect.topleft = (bstx+mwidth/2-bwidth/2+5,bsty+tbheight+5)
		pygame.draw.rect(window,bgColor,(bstx,bsty,mwidth+10,mheight+10))
		window.blit(tbstText,tbstRect)
		window.blit(bestText,bestRect)

		btopx,btopy,bColor = 425,100,(130,102,68)
		buttonFont = pygame.font.Font(None,30)
		buttonText = buttonFont.render("New Game",True,WHITE,bColor)
		bwidth,bheight = buttonFont.size("New Game")
		buttonRect = buttonText.get_rect()
		buttonRect.topleft = btopx+7.5,btopy+7.5
		pygame.draw.rect(window,bColor,(btopx,btopy,bwidth+15,bheight+15))
		window.blit(buttonText,buttonRect)

	def generateTile(self):

		emptyTile,emptySize = [],0
		for x in range (16):
			if (self.__block[x//4][x%4].value == 0):
				emptyTile.append(x)
				emptySize = emptySize + 1
		if (emptySize == 0):
			return
		x , p = random.randint(0,emptySize-1) , random.randint(0,9)
		i , j = emptyTile[x]//4 , emptyTile[x]%4
		if (p<9):
			self.__block[i][j].value = 2
		else:
			self.__block[i][j].value = 4

	def moveTiles(self,x,y):
		startx,endx,stepx = 0,4,1
		starty,endy,stepy = 0,4,1
		if (x > 0):
			startx,endx,stepx = 3,-1,-1 
		if (y > 0):
			starty,endy,stepy = 3,-1,-1
		for i in range (startx,endx,stepx):
			for j in range (starty,endy,stepy):
				if (self.__block[i][j].value == 0):
					continue
				nx,ny = i,j
				while (nx+x >= 0 and nx+x < 4 and ny+y >=0 and ny+y<4):
					if (self.__block[nx+x][ny+y].value>0):
						break
					nx = nx + x
					ny = ny + y
				if (nx == i and ny == j):
					continue
				tempval = self.__block[i][j].value
				self.__block[i][j].value = 0
				self.__block[nx][ny].value = tempval
				self.moveMade = True
		for i in range (startx,endx,stepx):
			for j in range (starty,endy,stepy):
				if (self.__block[i][j].value == 0):
					continue
				nx,ny = x+i,y+j
				if (nx>=0 and nx<4 and ny>=0 and ny<4):
					if (self.__block[nx][ny].value == self.__block[i][j].value):
						self.__block[nx][ny].value = 2*self.__block[i][j].value
						self.__block[i][j].value = 0
						self.__score = self.__score + self.__block[nx][ny].value
						self.highscore = max(self.highscore,self.__score)
						self.moveMade = True
		for i in range (startx,endx,stepx):
			for j in range (starty,endy,stepy):
				if (self.__block[i][j].value == 0):
					continue
				nx,ny = i,j
				while (nx+x >= 0 and nx+x < 4 and ny+y >=0 and ny+y<4):
					if (self.__block[nx+x][ny+y].value>0):
						break
					nx = nx + x
					ny = ny + y
				if (nx ==  i and ny == j):
					continue
				tempval = self.__block[i][j].value
				self.__block[i][j].value = 0
				self.__block[nx][ny].value = tempval
				self.moveMade = True

	def checkGameOver(self):
		foundZero,foundMove = False,False
		for i in range (0,4):
			for j in range (0,4):
				if (self.__block[i][j].value == 2048):
					self.gameOver = True
					self.message = "You Won!"
					return
				elif (self.__block[i][j].value == 0):
					foundZero = True
		if (not foundZero):
			px,py = [0,0,1,-1],[1,-1,0,0]
			for i in range (0,4):
				for j in range (0,4):
					for k in range (0,4):
						nx,ny = i+px[k],j+py[k]
						if (nx>=0 and ny>=0 and nx<4 and ny<4):
							if (self.__block[nx][ny].value == self.__block[i][j].value):
								foundMove = True
			if (not foundMove):
				self.gameOver = True
				self.message = "Game Over!"


	def checkNewGame(self):
		posx,posy = pygame.mouse.get_pos()
		btopx,btopy,bbotx,bboty = 425,100,545,138
		if (posx>=btopx and posx<=bbotx and posy>= btopy and posy<=bboty):
			return True

	def getScore(self):
		return self.__score