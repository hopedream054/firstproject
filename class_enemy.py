import game_framework
import math
from pico2d import*


class Enemy:                        #적1 바스티온 기관총
    def __init__(self,xx,yy):
        self.x=xx
        self.y=yy
        self.frame=0
        self.hp=30
        self.sence=0
        self.damage = 100
        self.image = load_image('enemy.png')
        self.bulletcount=0
    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
    def update(self,xx,yy):
        if self.bulletcount>0:
            self.bulletcount=(self.bulletcount+1)%20

        if self.sence==1:
            self.frame=(self.frame+1)%2
        else:
            self.frame=0
    def get_bb(self):
        return self.x-30,self.y-30,self.x+30,self.y+50

    def get_aa(self):
        return self.x, self.y

    def sence_hero(self,dd):
        if dd==True:
            self.sence=1
        else:
            self.sence=0
    def HP_state(self,a):
        self.hp=self.hp-a
    def get_hp(self):
        return self.hp
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_bulletcount(self):
        if self.bulletcount<12: return True #이것과 위의 불렛카운트를 이용하여 발사를 조절할수있음
        else: return False
    def up_bulletcount(self):
        self.bulletcount =self.bulletcount+ 1
    def get_damage(self):
        return self.damage

class Enemybullet:
    def __init__(self, xx,yy):
        self.x=xx
        self.y=yy
        self.speed=30
        self.damage = 10
        self.image = load_image('enemybullet.png')
    def draw(self):
        self.image.clip_draw(0, 0, 16, 30, self.x, self.y)
    def update(self):
        if self.y>-100:
            self.y=self.y-self.speed
    def get_bb(self):
        return self.x-8,self.y-15,self.x+8,self.y+15
    def get_y(self):
        return self.y
    def get_damage(self):
        return self.damage






class Boss:                        #보스
    def __init__(self):
        self.x=500
        self.y=800
        self.frame=0
        self.hp=400
        self.gox=-300
        self.goy=0
        self.xspeed=-30
        self.yspeed=0
        self.damage = 100
        self.image = load_image('boss.png')
        self.pattern=0
        self.tanframe = 0
    def draw(self):
        self.image.clip_draw(self.frame * 500, 0, 500, 250, self.x, self.y)
    def update(self):
        self.frame=(self.frame+1)%3
        self.tanframe = (self.tanframe + 1) % 10

        if self.gox:
            if self.gox>0 and self.gox-self.xspeed<=0:
                self.x+=self.xspeed
                self.xspeed=0
                self.gox=0
                self.gox=-300
                self.xspeed = -30
            elif self.gox<0 and self.gox-self.xspeed>=0:
                self.x+=self.xspeed
                self.xspeed=0
                self.gox=0
                self.gox = 300
                self.xspeed = 30
            else:
                self.x+=self.xspeed
                self.gox -= self.xspeed

        if self.goy:
            if self.goy>0 and self.goy-self.yspeed<0:
                self.y+=self.goy
                self.yspeed=0
                self.goy=0
            elif self.goy<0 and self.goy-self.yspeed>0:
                self.y+=self.goy
                self.yspeed=0
                self.goy=0
            else:
                self.y+=self.yspeed
                self.goy -= self.yspeed
    def get_bb(self):
        return self.x-250,self.y-80,self.x+250,self.y+100

    def get_aa(self):
        return self.x, self.y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    def HP_state(self,a):
        self.hp=self.hp-a
    def get_hp(self):
        return self.hp
    def get_damage(self):
        return self.damage
    def get_tanframe(self):
        return self.tanframe

class Bossbullet:
    def __init__(self, xx,yy,tx,ty):
        self.x=xx
        self.y=yy
        self.targetx = tx
        self.targety = ty

        print(xx)
        print(yy)
        tot=math.sqrt(tx * tx + ty * ty)
        print(tot)
        if tot<500: tot=500
        if tot>750: tot=500
        self.speedx= (tx-xx)/(tot/20)
        self.speedy= (ty-yy)/(tot/20)

        self.damage = 10
        self.frame = 0
        self.image = load_image('bosstan.png')
    def draw(self):
        self.image.clip_draw(self.frame*50, 0, 50, 50, self.x, self.y)
    def update(self):
        self.frame = (self.frame + 1) % 3
        self.y=self.y+self.speedy
        self.x = self.x + self.speedx
    def get_bb(self):
        return self.x-23,self.y-23,self.x+23,self.y+23
    def get_y(self):
        return self.y
    def get_x(self):
        return self.x
    def get_damage(self):
        return self.damage
