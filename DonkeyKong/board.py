import pygame
from pygame.locals import *

import random
import sprites
import positions
import player 

class Board():
    height=[] # pos of floor
    not_p=[] #pos of platforms
    h=[] #ladder positions
    l=[] #pos where there is no ladder
    wall_list=[]
    lad_pos=[]
    status=1
    #set screen
    pygame.init()
    screen=pygame.display.set_mode((1024,800))#blank screen displays
    pygame.display.set_caption("Donkey Kong")

    #set background music
    pygame.mixer.init()
    hit_coin=   pygame.mixer.Sound("audio/shoot.wav")
    hit_enemy=pygame.mixer.Sound("audio/enemy.wav")
    hit_coin.set_volume(0.05)
    hit_enemy.set_volume(0.05)

    pygame.mixer.music.load('audio/moonlight.wav')
    pygame.mixer.music.play(-1,0.0)
    pygame.mixer.music.set_volume(0.25)

    #font of all labels
    myfont=pygame.font.SysFont("Comic Sans MS",30)
    #"X" for score
    label_step=myfont.render("X",1,(255,255,255))
    #background image
    background=pygame.image.load("images/bg.jpg").convert()
    m=background.get_width()
    n=background.get_height()

    #health bar

    life3=pygame.image.load("images/life3.jpg").convert()
    life2=pygame.image.load("images/life2.jpg").convert()
    life1=pygame.image.load("images/life1.gif").convert()

    #princess
    princess=pygame.image.load("images/princess.gif").convert()

    #coin for score
    sc_coin=pygame.image.load("images/coin.gif").convert()
    gameover=pygame.image.load("images/gameover.jpg").convert()
    fonts=pygame.font.SysFont("Comic Sans MS",70)
    label_gameover=fonts.render("GAMEOVER",1,(255,255,255))
    try_again=fonts.render("TRY AGAIN",1,(255,255,255))
    fonts=pygame.font.SysFont("Comic Sans MS",50)
    label_sc=fonts.render("SCORE:",1,(255,255,255))


    def __init__(self,width,ht,stat):
        self.screen_width=width
        self.screen_height=ht
        self.status=stat
        
        pass

    def getAllElements(self):
        Board.wall_list=positions.border()
        Board.height=positions.floorHeight()
        Board.lad_pos=positions.floorOpening()
        positions.ladderPositions()
        #place the coins
        positions.coinPosition()
        positions.wallPosition()

    #main function
    def setBoard(self):

        p=player.Player()

        #fireball
        fireball=sprites.FireBall()

        clock=pygame.time.Clock()

        #timer for fireball
        pygame.time.set_timer(USEREVENT+1,5000)

        #call donkey
        donkey=sprites.Donkey()

        #ladder positions
        while 1:
            self.screen.fill((255,255,255))

            for x in range(self.screen_width/Board.m+1):
                for y in range(self.screen_height/Board.n+1):
                    Board.screen.blit(Board.background,(x*100,y*100))


            #draw screen border
            sprites.Border.border_list.draw(Board.screen)
            #draw platforms
            sprites.Platform.platform_list.draw(Board.screen)

            #place the player
            player.Player.playr.draw(Board.screen)
            #draw the coins
            sprites.Coin.coin_list.draw(Board.screen)
            #draw ladder
            sprites.Ladder.ladder_list.draw(Board.screen)
            #draw walls
            sprites.Wall.wall_list.draw(Board.screen)
            #get level

            #display score
            label_score=Board.myfont.render(str(p._scores),1,(255,255,255))
            Board.screen.blit(Board.sc_coin,(1024-100,40))
            Board.screen.blit(Board.label_step,(1024-75,40))
            Board.screen.blit(label_score,(1024-50,40))

            #health bar
            if p.lifes==3:
                Board.screen.blit(Board.life3,(40,37))
            elif p.lifes==2:
                Board.screen.blit(Board.life2,(40,37))
            elif p.lifes==1:
                Board.screen.blit(Board.life1,(40,37))

            #princess

            Board.screen.blit(Board.princess,(290,90-34)) 

            #fireball
            fireball.level()
            sprites.FireBall.fire_ball_list.update()
            sprites.FireBall.fire_ball_list.draw(Board.screen)


            #donkey
            donkey.move()

            if Board.status!=0:
            #p.playerMove()
                p.update()
                p.collectCoin()
                p.level()
                p.checkWall()
                fireball_hit=pygame.sprite.spritecollide(p,sprites.FireBall.fire_ball_list,False)
                for hit in fireball_hit:
                    p._scores-=25
                    Board.hit_enemy.play()
                    p.reset()
                    break

                for event in pygame.event.get():
                    p.getPosition()

                    if event.type==USEREVENT+1:
                        fireball=sprites.FireBall()

                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_LEFT:
                            p.speed_x=-6

                        if event.key==pygame.K_RIGHT:
                            p.speed_x=6

                        if event.key==pygame.K_SPACE:
                            p.jump()

                        if event.key==pygame.K_UP:
                            if p.lad_bottom==1 or p.on_ladder==1:
                                p.on_ladder=1
                                p.climbUp()
                            else:
                                pass
                        if event.key==pygame.K_DOWN:
                            if p.lad_top==1 or p.on_ladder==1:
                                p.on_ladder=1
                                p.climbDown()

                        if event.key==pygame.K_q:
                            pygame.quit()
                            exit(0)

                    if event.type==pygame.KEYUP:
                        if event.key==pygame.K_LEFT and p.speed_x<0:
                            p.stop()

                        if event.key==pygame.K_RIGHT and p.speed_x>0:
                            p.stop()

                        if event.key==pygame.K_UP:
                            p.stop()

                        if event.key==pygame.K_DOWN:
                            p.stop()
                            pass


                    if event.type==pygame.QUIT:
                        pygame.quit()
                        exit(0)

            else:
                Board.screen.blit(Board.gameover,(200,200))
                Board.screen.blit(Board.label_gameover,(400,320))
                Board.screen.blit(Board.label_sc,(440,390))

                Board.screen.blit(Board.try_again,(400,450))
                pre_score=Board.fonts.render(str(p._scores),1,(255,255,255))
                Board.screen.blit(pre_score,(590,390))


                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        exit(0)


            clock.tick(60)
            #update screen
            pygame.display.flip()


            

