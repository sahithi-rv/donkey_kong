import pygame
from pygame.locals import *

import sprites
import positions
import board


class Player(pygame.sprite.Sprite): #inherits pygame sprites class
	playr=pygame.sprite.Group()
	def __init__(self):

		pygame.sprite.Sprite.__init__(self)
		width=40
		height=50
		sch=30
		self.flag=0
		self.image=pygame.image.load("images/player.gif").convert()
		self.rect=self.image.get_rect()
		self.direction_x=0
		self.direction_y=0
		self.speed_x=0
		self.speed_y=0
		self.levels=0
		self.rect.x=width
		#self.rect.y=800-height-sch
		self.rect.y=800-20-30
		self._scores=0		#protected
		self.lifes=3
		self._gravity=1
		self._force=0
		self.on_ladder=0
		self.lad_bottom=0
		self.lad_top=0
		self.platform_hit_list=[]
		self.ladder_hit_list=[]

		Player.playr.add(self)


	def update(self):
		if self.on_ladder==0:
			self.cal_gravity()

		self.rect.x+=self.speed_x
		border_hit_list=pygame.sprite.spritecollide(self,sprites.Border.border_list,False)
		for block in border_hit_list:
			if self.speed_x>0:
				self.direction_x=-1
				self.rect.right=block.rect.left

			elif self.speed_x<0:
				self.direction_x=1
				self.rect.left=block.rect.right

		self.rect.y+=self.speed_y

		platform_hit_list=pygame.sprite.spritecollide(self,sprites.Platform.platform_list,False)
		for block in platform_hit_list:
				if self.speed_y>0:
					self.rect.bottom=block.rect.top

				elif self.speed_y<0:
					self.rect.top=block.rect.bottom

				self.speed_y=0

	def checkCollision(self):
		self.rect.y+=10
		self.ladder_hit_list=pygame.sprite.spritecollide(self,sprites.Ladder.ladder_list,False)
		self.rect.y-=10

		self.rect.y+=10
		self.platform_hit_list=pygame.sprite.spritecollide(self,sprites.Platform.platform_list,False)
		self.rect.y-=10		

	def getPosition(self):
		self.checkCollision()

		if len(self.platform_hit_list)>0 and len(self.ladder_hit_list)>0:
			self.flag=1
			self.lad_bottom=1
			#self.rect.bottom=self.platform_hit_list[0].rect.top
			self._force=0

		elif len(self.platform_hit_list)==0 and len(self.ladder_hit_list)>0 and self.ladder_hit_list[0].rect.y in range(self.rect.y-10,self.rect.y+10):
			self.lad_top=1
			self._force=0

		elif len(self.platform_hit_list)==0 and len(self.ladder_hit_list)>0:
			self.on_ladder=1
			self._force=self._gravity
		else:
			self.on_ladder=0
			self.lad_top=0
			self.lad_bottom=0
			self._force=0

		return (self.rect.x,self.rect.y)

	def cal_gravity(self):
		if self.speed_y==0:
			self.speed_y=1
		else:
			self.speed_y+=self._gravity-self._force

		if self.rect.y>=(1024)-30 - self.rect.height and self.speed_y>=0:
			self.speed_y=0
			self.rect.y=(1024)-30 - self.rect.height

	def jump(self):
		self.rect.y+=10
		platform_hit_list=pygame.sprite.spritecollide(self,sprites.Platform.platform_list,False)
		self.rect.y-=10

		if len(platform_hit_list)>0:
			self.speed_y=-10

	def climbUp(self):
		#self.force=self.gravity
		self.speed_y=-2
		self.rect.y+=10
		platform_hit_list=pygame.sprite.spritecollide(self,sprites.Platform.platform_list,False)
		self.rect.y-=10
		


	def climbDown(self):
		#self.force=self.gravity
		self.speed_y=2
		platform_hit_list=pygame.sprite.spritecollide(self,sprites.Platform.platform_list,False)

		pass

	def stop(self):
		self.speed_x=0
		self.speed_y=0

	def collectCoin(self):
		coin_hit=pygame.sprite.spritecollide(self,sprites.Coin.coin_list,True)
		for hit in coin_hit:
			board.Board.hit_coin.play()
			self._scores+=5

	def gameover(self):
		board.Board.status=0

	def reset(self):
		if self.lifes>0:
			self.lifes-=1
			self.rect.x=50
			self.rect.y=800-30-25
			fireball=sprites.FireBall()

		else:
			self.gameover()

	def level(self):
		for i in range(0,7):
			if self.rect.y <=board.Board.height[i] and self.rect.y>=board.Board.height[i+1]:
				self.levels=i

		if self.levels==6:
			self._scores+=50
			board.Board.status+=1
			if board.Board.status>2:
				self.gameover()
			else:
				self.lifes=3
				for coin in sprites.Coin.coin_list:
					sprites.Coin.coin_list.remove(coin)
				positions.coinPosition()

				for fireball in sprites.FireBall.fire_ball_list:
					sprites.FireBall.fire_ball_list.remove(fireball)
				self.reset()
			pass

	def checkWall(self):
		wall_hit_list=pygame.sprite.spritecollide(self,sprites.Wall.wall_list,False)

		for block in wall_hit_list:
			if self.speed_x>0:
				self.direction_x=-1
				self.rect.right=block.rect.left

			elif self.speed_x<0:
				self.direction_x=1
				self.rect.left=block.rect.right

	def score(self):
		return self._scores





