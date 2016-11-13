import random
import json
import os


from pico2d import *
import game_framework

mainhero=None
total_frametime=None
x_right=x_left=y_up=y_down=None


bastion=[]
baseatack=[]


class Luci:                   #메인캐릭터
    def __init__(self,xx,yy):
        self.frame=random.randint(0, 8)
        self.x=xx
        self.y=yy
        self.speed=20

        self.image=load_image('luci_character.png')

    def transxy(self,xx,yy):
        self.x+=xx
        self.y+=yy


    def update(self):
        global x_right, x_left, y_up, y_down


        self.frame=(self.frame+1)%8

        if x_right == True and self.x <= 760:
            self.x = self.x + self.speed
        if x_left == True and self.x >= 140:
            self.x = self.x - self.speed
        if y_up == True and self.y < 960:
            self.y = self.y + self.speed
        elif y_down == True and self.y > 40:
            self.y = self.y - self.speed



    def draw(self):
        self.image.clip_draw(self.frame * 80, 0, 80, 100, self.x, self.y)

    def get_bb(self):
        return self.x-40,self.y-40,self.x+50,self.y+50
    def get_aa(self):
        return self.x, self.y
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y



class bullet:                  #주인공 기본 탄환

    def __init__(self,xx,yy):
        self.x=xx
        self.y=yy
        self.speed=30
        self.damage=10
        self.image = load_image('soundwave.png')

    def draw(self):
        print('c')
        self.image.clip_draw(0, 0, 30, 30, self.x, self.y)

    def update(self):
        self.y=self.y+self.speed
    def get_bb(self):
        return self.x-15,self.y-15,self.x+15,self.y+15
    def get_y(self):
        return self.y
    def get_damage(self):
        return self.damage

class Enemy:                        #적1 바스티온 기관총
    def __init__(self,xx,yy):
        self.x=xx
        self.y=yy
        self.frame=0
        self.hp=30
        self.sence=0
        self.image = load_image('enemy.png')
    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
    def update(self,xx,yy):
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

    def Hp_state(self,damage):
        self.hp-=damage
        if self.hp<=0:
            return True
        return False
    def get_hp(self):
        return self.hp




def enter():
    global mainhero,total_frametime
    global x_right,x_left,y_up,y_down #키의 상태값
    global bastion

    total_frametime=0
    mainhero=Luci(300,800)

    bastion.append(Enemy(300,900))

    x_right = x_left = y_up = y_down=False

def exit():
    global mainhero
    del(mainhero)

def update(frame_time):
    global mainhero, baseatack
    global total_frametime
    global bastion

    total_frametime+= frame_time


    if total_frametime>0.1:
        total_frametime=0
        mainhero.update()


        basei=[]#지워야할 탄을 저장함
        for i in range(len(baseatack)):
            baseatack[i].update()
            if 1000<baseatack[i].get_y():
                basei.append(i)


        if len(basei)>0: #탄이 멀리 나갔을때 지운다.
            basetemp=0
            for i in range(len(basei)):
                del baseatack[basei[i]-basetemp]
                ++basetemp

        basti = []
        #for i in range(len(baseatack)):
            #for j in range(len(bastion)):
                #if collide(bastion[j], baseatack[i]):
                    #del baseatack[i]

        for i in range(len(bastion)): #바스티온의 주인공 인식
            bastion[i].update(mainhero.get_x,mainhero.get_x)
            dota=bastion_sence(bastion[i] , mainhero)
            bastion[i].sence_hero(dota)

        #입력받은 값으로 주인공의 위치 변경


def draw(frame_time):
    global mainhero, baseatack
    global bastion

    clear_canvas()
    mainhero.draw()

    for i in range(len(baseatack)):
        baseatack[i].draw()

    for i in range(len(bastion)):
        bastion[i].draw()

    update_canvas()

def handle_events(frame_time):
    global x_right, x_left, y_up, y_down
    global mainhero,baseatack
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                x_right = True
            elif event.key == SDLK_LEFT:
                x_left = True
            elif event.key == SDLK_UP:
                y_up = True
            elif event.key == SDLK_DOWN:
                y_down = True
            if event.key == SDLK_SPACE:
                baseatack.append(bullet(mainhero.get_x(),mainhero.get_y()))
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                x_right = False
            elif event.key == SDLK_LEFT:
                x_left = False
            elif event.key == SDLK_UP:
                y_up = False
            elif event.key == SDLK_DOWN:
                y_down = False

def collide(a,b):  #a:anemy b:tan
    left_a,bottom_a,right_a,top_a=a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a>right_b: return False
    if right_a<left_b: return False
    if top_a< bottom_b: return False
    if bottom_a> top_b: return False

    return True

def bastion_sence(aa,bb):
    left_a, bottom_a, right_a, top_a = aa.get_bb()
    x ,y =bb.get_aa()

    if left_a>x : return False
    if right_a<x: return False
    if bottom_a<y: return False

    return True