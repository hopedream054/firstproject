import game_framework
import math
import random
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
    def update(self,worldspeed):
        self.y=self.y-worldspeed

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
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def bastion_sence(self, bb):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        x, y = bb.get_aa()

        if left_a > x: return False
        if right_a < x: return False
        if bottom_a < y: return False
        if bottom_a - y < 200: return False
        return True

class Enemybullet:
    def __init__(self, xx,yy):
        self.x=xx
        self.y=yy
        self.speed=20
        self.damage = 10
        self.image = load_image('enemybullet.png')
    def draw(self):
        self.image.clip_draw(0, 0, 16, 30, self.x, self.y)
    def update(self,worldspeed):
        if self.y>-100:
            self.y=self.y-self.speed-worldspeed
    def get_bb(self):
        return self.x-8,self.y-15,self.x+8,self.y+15
    def get_y(self):
        return self.y
    def get_damage(self):
        return self.damage
    def draw_bb(self):
        draw_rectangle(*self.get_bb())






class Enemy_second:                        #적2 라인하르트
    def __init__(self,xx,yy):
        self.x=xx
        self.y=yy
        self.frame=0
        self.hp=30
        self.sence=0
        self.atacktime=0
        self.damage = 100


        self.state=3 #상태  1번 대기 2번 공격 3번 가드
        self.shild_hp=40

        self.image_wait = load_image('Reinhardt_wait.png')
        self.image_guard = load_image('Reinhardt_guard.png')
        self.image_atack = load_image('Reinhardt_atack.png')
        self.image_shild = load_image('Reinhardt_shild.png')
        self.image_fire = load_image('Reinhardt_fire.png')

    def draw(self):
        if self.state==1: self.image_wait.clip_draw(self.frame%2 * 120, 0, 120, 180, self.x, self.y)
        elif self.state == 2:
            self.image_atack.clip_draw((int)(self.atacktime/10)*120, 0, 120, 180, self.x, self.y)
            if (int)(self.atacktime/10):
                self.image_fire.clip_draw((int)((self.atacktime-10)/2)*100, 0, 100, 100, self.x, self.y-100)
                self.image_fire.clip_draw((int)((self.atacktime-10)/2)*100, 0, 100, 100, self.x, self.y - 200)
                self.image_fire.clip_draw((int)((self.atacktime-10)/2)*100, 0, 100, 100, self.x-100, self.y - 200)
                self.image_fire.clip_draw((int)((self.atacktime-10)/2)*100, 0, 100, 100, self.x+100, self.y - 200)

        elif self.state == 3:
            self.image_guard.clip_draw(0, 0, 120, 180, self.x, self.y)
            if self.shild_hp>0: self.image_shild.clip_draw(0, 0, 240, 200, self.x, self.y)

    def update(self,worldspeed):
        self.y=self.y-worldspeed

        self.frame=self.frame+1

        if self.state==2:
            self.atacktime=self.atacktime+1
            if self.atacktime>=20:
                print('zxasqw')
                self.atacktime=0
                self.state=1
        elif self.state!=2 and self.frame>=40:
            self.frame=0
            self.state=3
            self.shild_hp=40

    def create_shild(self):
        self.shild_hp=4

    def get_bb(self):
        if self.shild_hp>0 and self.state==3: return self.x - 120, self.y - 100, self.x + 120, self.y + 90
        else: return self.x-60,self.y-90,self.x+60,self.y+30

    def get_aa(self):
        return self.x, self.y
    def sence_hero(self,dd):
        if dd==True:
            self.sence=1
        else:
            self.sence=0
    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def reinhardt_sence(self, bb):
        left_a=self.x-60
        bottom_a=self.y-90
        right_a=self.x+60
        top_a = self.y+30
        x, y = bb.get_aa()

        if left_a > x: return False
        if right_a < x: return False
        if bottom_a < y: return False
        if bottom_a - y > 200: return False
        return True

class reinhartd_fire:                        #적2 라인하르트
    def __init__(self,xx,yy):
        self.x=xx
        self.y=yy
        self.damage = 100
        self.frame=0
        self.image_fire = load_image('Reinhardt_fire.png')

    def draw(self):
        self.image_fire.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y-100)

    def update(self,worldspeed):
        self.frame=(self.frame+1)%5

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50
    def draw_bb(self):
        draw_rectangle(*self.get_bb())




class Enemy_third:                        #적3 겐지
    def __init__(self,xx,yy):
        self.x=xx
        self.y=yy
        self.frame=0
        self.hp=30
        self.sence=0
        self.atacktime=0
        self.damage = 100
        self.speed_x=15
        self.speed_y=0
        if yy>350:
            self.dir = -1
        else:
            self.dir = 1

        self.state=1 #상태  1번 대기 2번 그림자소환

        self.shild_hp=40

        self.image = load_image('genji.png')

    def draw(self):
        self.image.clip_draw(0, 0, 100, 100, self.x, self.y)
    def update(self,worldspeed):
        self.y = self.y - worldspeed-self.speed_y
        self.x = self.x + self.dir * self.speed_x

        if self.state==1:
            if self.frame==19:
                self.state=2
                self.dir=random.randint(-1, 1)
                self.speed_x = 15
                self.speed_y = 30

            self.frame=(self.frame+1)%20

        elif self.state == 2:
            if self.frame==9:
                self.state=1
                self.speed_x = 15
                self.speed_y = 0
                if self.x > 350:
                    self.dir = -1
                else:
                    self.dir = 1



            self.frame=(self.frame+1)%10
    def get_bb(self):
        return self.x-50,self.y-50,self.x+50,self.y+50

    def get_aa(self):
        return self.x, self.y

    def draw_bb(self):
        draw_rectangle(*self.get_bb())



class Genji_shot:
    def __init__(self, xx,yy,dirspeed):
        self.x=xx
        self.y=yy
        self.speedy=20
        self.speedx=dirspeed
        self.frame=0
        self.damage = 10
        self.image = load_image('genji_atack.png')

    def draw(self):
        self.image.clip_draw(self.frame*40, 0, 40, 40, self.x, self.y)

    def update(self,worldspeed):
        self.frame=(self.frame+1)%3
        if self.y>-100:
            self.y=self.y-self.speedy-worldspeed
            self.x = self.x - self.speedx

    def get_bb(self):
        return self.x-15,self.y-15,self.x+15,self.y+15
    def get_y(self):
        return self.y
    def get_damage(self):
        return self.damage
    def draw_bb(self):
        draw_rectangle(*self.get_bb())



class Genji_shadow:
    def __init__(self, xx,yy,num):
        self.x=xx
        self.y=yy
        self.frame=0
        self.damage = 100
        self.image = load_image('genji_shadow.png')
        self.number=num%4
    def draw(self):
        self.image.clip_draw(self.number*100, 0, 100, 100, self.x, self.y)

    def update(self,worldspeed):
        self.y = self.y- worldspeed/2
        self.frame=self.frame+1

    def get_bb(self):
        return self.x-50,self.y-50,self.x+50,self.y+50
    def draw_bb(self):
        draw_rectangle(*self.get_bb())














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

        if self.pattern==0:
            if self.gox:
                if self.gox > 0 and self.gox - self.xspeed <= 0:
                    self.x += self.xspeed
                    self.xspeed = 0
                    self.gox = 0
                    print(self.x)
                    self.gox = -(self.x - 250)
                    self.xspeed = -30
                elif self.gox < 0 and self.gox - self.xspeed >= 0:
                    self.x += self.xspeed
                    self.xspeed = 0
                    self.gox = 0
                    print(self.x)
                    self.gox = (800 - self.x) - 250
                    self.xspeed = 30
                else:
                    self.x += self.xspeed
                    self.gox -= self.xspeed

            if self.goy:
                if self.goy > 0 and self.goy - self.yspeed < 0:
                    self.y += self.goy
                    self.yspeed = 0
                    self.goy = 0
                elif self.goy < 0 and self.goy - self.yspeed > 0:
                    self.y += self.goy
                    self.yspeed = 0
                    self.goy = 0
                else:
                    self.y += self.yspeed
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
    def draw_bb(self):
        draw_rectangle(*self.get_bb())


class Bossbullet:
    def __init__(self, xx,yy,tx,ty):
        self.x=xx
        self.y=yy
        self.targetx = tx
        self.targety = ty

        tot=math.sqrt(tx * tx + ty * ty)
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
        return self.x-25,self.y-25,self.x+25,self.y+25
    def get_y(self):
        return self.y
    def get_x(self):
        return self.x
    def get_damage(self):
        return self.damage
    def draw_bb(self):
        draw_rectangle(*self.get_bb())

