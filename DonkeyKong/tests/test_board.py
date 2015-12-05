from board import Board
from player import Player
import positions
import sprites
import pytest
from pygame.locals import *

@pytest.fixture()
def screen():
	return Board(1024,800,1)

@pytest.fixture()
def gamer():
	return Player()

@pytest.fixture()
def villain(screen):
	screen.getAllElements()
	return sprites.Donkey()

@pytest.fixture()
def obstacle():
	return sprites.FireBall()


class TestScreen:
#	def __init__(self):
#		pass

	def test_board(self,screen):
		assert screen.screen_width == 1024
		assert screen.screen_height == 800

	def test_positions(self,screen):
		screen.getAllElements()
		assert len(Board.height)>0
		assert len(Board.wall_list)>0
		assert len(Board.lad_pos)>0


class TestPerson:

#	def __init__(self):
#		pass

	def test_movement(self,screen,gamer):
		gamer.update()
		tup=gamer.getPosition()
		#print screen.screen_width
		#print tup
		#print gamer.rect.x 
		assert tup[0] <= (screen.screen_width-30)  and tup[0] >= 30 and tup[1] <= (screen.screen_height-10) and tup[1]>=10

	#check force and gravity
	def test_attr(self,gamer,screen):
		positions.floorHeight()
		lad_pos=positions.floorOpening()
#	#print lad_pos
		for y in range(1,5):
			for x in range(30,screen.screen_width-30,6):
				gamer.getPosition()
				gamer.checkCollision()
				if x in lad_pos[y]:
				#print x
					if len(gamer.platform_hit_list)==0 and len(gamer.ladder_hit_list)>0:
						assert gamer._force == gamer._gravity
						check_climbUp(gamer)
					else:
						assert gamer._force == 0

	#check climbup
	def check_climbUp(self,gamer):
		tup1=gamer.getPosition()
	
		gamer.climbUp()
		gamer.update()
		tup2=gamer.getPosition()
		assert tup1[1]-2 == tup2[1]

	def test_motionRight(self,gamer,screen):
		tup1=gamer.getPosition()
		gamer.speed_x=6
		for i in range(100):
			if gamer.rect.x<=screen.screen_width-30:
				gamer.update()
				tup2=gamer.getPosition()
				assert tup1[0]+6 == tup2[0]
				tup1=tup2

	def test_motionLeft(self,gamer,screen):
		tup1=(900,740)
		(gamer.rect.x,gamer.rect.y)=tup1
		gamer.speed_x=-6
		for i in range(100):
			if gamer.rect.x<=screen.screen_width-30:
				gamer.update()
				tup2=gamer.getPosition()
				assert tup1[0]-6 == tup2[0]
				tup1=tup2

	def test_checkCollision(self,gamer):
		gamer.checkCollision()
		assert len(gamer.platform_hit_list)>0

	def test_score(self,gamer):
		positions.coinPosition()
		sc=gamer.score()
		li=[58,243,486,789,976]
		for x in li:
			sc=gamer.score()
			gamer.rect.x=x
			gamer.collectCoin()
			sc1=gamer.score()
			assert sc+10 == sc1

	def checkPos(self,gamer):
		
		if gamer.rect.x <0:
			raise ValueError('adfssdf')

	def test_checkPos(self,gamer):
		gamer.rect.x=-1
		with pytest.raises(ValueError):
			self.checkPos(gamer)


class TestVillain:

#	def __init__(self):
#		pass

#check donkey movement
	def test_villain(self,villain,screen):
	#screen.getAllElements()
		for i in range(100):
			villain.move()
			assert villain.rect.x <= screen.screen_width/3 and villain.rect.x >= 30

	def checkdonkey(self,screen,villain):
		if villain.rect.x > screen.screen_width/3 or villain.rect.x <30:
			raise ValueError("sdf")

	def test_donkey(self,villain,screen):
		villain.rect.x=700
		with pytest.raises(ValueError):
			self.checkdonkey(screen,villain)

		villain.rect.x=10	
		with pytest.raises(ValueError):
			self.checkdonkey(screen,villain)

class TestFireball:
#	def __init__(self):
#		pass

	def test_fireball(self,obstacle,screen):
		for i in range(100):
			obstacle.update()
			assert obstacle.rect.x <= (screen.screen_width-30)  and obstacle.rect.x >= 30 and obstacle.rect.y <= (screen.screen_height-10) and obstacle.rect.y>=10

	def test_gravity(self,obstacle):
		for i in range(100):
			obstacle.update()
			assert obstacle._gravity > 0


class TestSpritePositions:

	def checkladderpos(self,screen):
		positions.floorHeight()
		lad_pos=positions.floorOpening()
		for y in range(1,5):
			for x in lad_pos[y]:
				if x >= 30 and x<= (1024-30):
					raise ValueError('adfssdf')	

	def test_ladder(self):
		with pytest.raises(ValueError):
			self.checkladderpos(screen)

	
