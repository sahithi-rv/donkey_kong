import pygame
from pygame.locals import * 

import board
import random

class Border(pygame.sprite.Sprite):
    border_list=pygame.sprite.Group()   #sprite group to store boundaries
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image=img
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def addSprite(self):
        Border.border_list.add(self)




class Platform(Border):                 #inherits the properties from border class
    platform_list=pygame.sprite.Group()
    def __init__(self,x,y,img):
        Border.__init__(self,x,y,img)

    def addSprite(self):                #polymorphism
        Platform.platform_list.add(self)

class Coin(pygame.sprite.Sprite):
    coin_list=pygame.sprite.Group() # sprite group to store coin sprites 
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self) # calling the super class's init
        self.image=pygame.image.load("images/coin.gif").convert()
        self.rect=self.image.get_rect()
        self.rect.topleft=pos
        Coin.coin_list.add(self)


class FireBall(pygame.sprite.Sprite):
    fire_ball_list=pygame.sprite.Group()
    HEIGHT=20
    WIDTH=20
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("images/fireball.gif").convert()
        self.rect=self.image.get_rect()
        self.levels=5
        self.speed_x=5
        self.speed_y=0
        self.direction_x=1
        self.direction_y=-1
        self._gravity=1
        self.rect.x=30
        self.rect.y=board.Board.height[self.levels]
        FireBall.fire_ball_list.add(self)
    
    def update(self):

        #print self.speed_x
        self.calc_gravity()
        self.rect.x+=self.speed_x
        border_hit=pygame.sprite.spritecollide(self,Border.border_list,False)
        #print len(border_hit)
        #print border_hit
        for block in border_hit:
         #   print block
          #  print self.speed_x
            if self.speed_x>0:
                self.direction_x=-1
                self.rect.right=block.rect.left
                self.speed_x*=-1
                break

            elif self.speed_x<0:
                self.speed_x*=-1
                self.direction_x=1
                self.rect.left=block.rect.right
                break

        self.rect.y+=self.speed_y

        platform_hit_list=pygame.sprite.spritecollide(self,Platform.platform_list,False)
        for block in platform_hit_list:
            if self.speed_y>0:
                self.rect.bottom=block.rect.top
            elif self.speed_y<0:
                self.rect.top=block.rect.bottom

            self.speed_y=0
        pass

    def calc_gravity(self):
        if self.speed_y==0:
            self.speed_y=1

        else:
            self.speed_y+=self._gravity

        if self.rect.y>=(1024)-30 - FireBall.HEIGHT and self.speed_y>=0 :
            self.speed_y=0
            self.rect.y=(1024)-30 - FireBall.HEIGHT

    def level(self):
        for i in range(0,7):
            if self.rect.y<=board.Board.height[i] and self.rect.y>=board.Board.height[i+1]:
                self.levels=i

    def jump(self):
        self.rect.y+=2
        platform_hit_list=pygame.sprite.spritecollide(self,Platform.platform_list,False)
        self.rect.y-=2

        if len(platform_hit_list)>0:
            self.speed_y=-10


class Donkey():
    def __init__(self):
        self.image_right=pygame.image.load("images/donkey1.gif").convert()
        self.image_left=pygame.image.load("images/donkey2.gif").convert()
        self.__image=self.image_right
        self.rect=self.__image.get_rect()
        self.rect.x=35
        self.rect.y=board.Board.height[5]-60
        self.speed_x=2.6
        self.direction_x=1
   
    def move(self):
        if self.rect.x>=1024*1/3:
            self.direction_x=-1
            self.__image=self.image_left
            self.speed_x=-2.6

        if self.rect.x<=20:
            self.speed_x=2.6
            self.__image=self.image_right

        board.Board.screen.blit(self.__image,(self.rect.x,self.rect.y))
        self.rect.x+=self.speed_x

class Ladder(pygame.sprite.Sprite):
    ladder_list=pygame.sprite.Group()
    def __init__(self,x,y1,y2,lev):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("images/ladder.gif")
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y1
        self.top_y=y1
        self.bottom_y=y2
        self.level=lev

    def addSprite(self):
        Ladder.ladder_list.add(self)


class Wall(pygame.sprite.Sprite):
    wall_list=pygame.sprite.Group()
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self) # calling the super class's init
        self.image=pygame.Surface([20,20])
        self.rect=self.image.get_rect()
        self.image.fill((176,162,162))
        self.rect.topleft=pos
        Wall.wall_list.add(self)





        


