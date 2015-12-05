import pygame
from pygame.locals import *

import board
import sprites
import player as player
import  random
height=[]
not_p=[]
h=[]
lad_pos=[]
dollar_list=[]
rem=0
HEIGHT=800
WIDTH=1024
def floorHeight():
	height.append(800-10)# 0 level
	height.append(627+40)#1
	height.append(504+40)#2
	height.append(381+40)#3
	height.append(258+40)#4
	height.append(135+40)#5
	height.append(50+40)#6
	height.append(0)#7
	return height

def border():
	vbrik=pygame.image.load("images/brick2.jpg")
	#hbrik=pygame.image.load("images/brick1.jpg")
	wall_list=[]
	for y in range(0,686,83):
		wall_list.append(y)
	for y in wall_list:
		b=sprites.Border(0,y,vbrik)
		b.addSprite()
	wall_list=[]
	for y in range(0,769,83):
		wall_list.append(y)

	for y in wall_list:
		p=sprites.Border(1024-30,y,vbrik)
		p.addSprite()

	b=sprites.Border(219,10,vbrik)
	b.addSprite()
	return wall_list	

def floorOpening():
	n=9
	hbrik=pygame.image.load("images/brick1.jpg")
	for j in range(1,6):#levels 1 to 5
		if j%2!=0:
			x=28
		else:
			x=215
		k=[]
		np=[]
		for i in range(n):
			if i==3:
				x+=5
				k.append(x)				
				x+=40
			if i==6:
				x+=5
				k.append(x)
				x+=40
			np.append(x)
			p=sprites.Platform(x,height[j],hbrik)
			p.addSprite()
			x+=83
		lad_pos.append(k)
		not_p.append(np)


	for x in range(28,995,83):#levels 0 and 7
		p=sprites.Platform(x,height[0],hbrik)
		p.addSprite()
		p=sprites.Platform(x,height[7],hbrik)
		p.addSprite()

	y=height[6]
	x=249
	for i in range(4):#level 6
		if i==2:
			x+=5
			x+=40
		p=sprites.Platform(x,y,hbrik)
		p.addSprite()
		x+=83

	return lad_pos
#function to find the positions of ladders
def ladderPositions():
	for i in range(1,6):
		l=sprites.Ladder(lad_pos[i-1][0],height[i],height[i-1],i)#height[i-1] > height[i]
		l.addSprite()
		l=sprites.Ladder(lad_pos[i-1][1],height[i],height[i-1],i)#height[i-1] > height[i]
		l.addSprite()		
	l=sprites.Ladder(425,height[6],height[5],6)
	l.addSprite()


#function to find the position of all coins
def coinPosition():
	if board.Board.status==1:
		dollar_list=[[58,243,486,789,976],[100,563,356],[478,240,720,547],[345,555,234],[301,407,511,843],[234,754]]

	elif board.Board.status==2:
		dollar_list=[[158,567],[666,322],[222,333,444,555],[464,323,545],[345,523,950],[]]


	for i in range(6):
		for x in dollar_list[i]:
			c=sprites.Coin((x,height[i]-20))

def wallPosition():
	wall_list=[[100,786],[70,689],[444,333],[],[366,912,666],[323]]

	for i in range(6):
		for x in wall_list[i]:
			w=sprites.Wall((x,height[i]-20))

def boardUpdate():
	board.Board.screen.fill((255,255,255))
	sprites.Border.border_list.draw(board.Board.screen)
	sprites.Platform.platform_list.draw(board.Board.screen)
	player.Player.playr.draw(board.Board.screen)
	sprites.Coin.coin_list.draw(board.Board.screen)
	for tup in board.Board.h:
		for y in range(tup[1],tup[2],12):
			board.Board.screen.blit(board.Board.label_step,(tup[0],y))

	pygame.display.flip()
    