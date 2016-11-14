import random
import json
import os


from pico2d import *
import game_framework

from class_enemy import Enemy,Enemybullet,Boss


mainhero=None
total_frametime=None
x_right=x_left=y_up=y_down=None

boss=None

bastion=[]
baseatack=[]
enemyatack=[]

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

        self.image.clip_draw(0, 0, 30, 30, self.x, self.y)

    def update(self):
        self.y=self.y+self.speed
    def get_bb(self):
        return self.x-15,self.y-15,self.x+15,self.y+15
    def get_y(self):
        return self.y
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






def enter():
    global mainhero,total_frametime
    global x_right,x_left,y_up,y_down #키의 상태값
    global bastion
    global boss
    total_frametime=0
    mainhero=Luci(300,800)

    bastion.append(Enemy(300,900))
    boss=Boss()
    x_right = x_left = y_up = y_down=False

def exit():
    global mainhero
    del(mainhero)

def update(frame_time):
    global mainhero, baseatack
    global total_frametime
    global bastion,enemyatack
    global boss

    total_frametime+= frame_time


    if total_frametime>0.1:
        total_frametime=0
        mainhero.update()


        basei=[]#지워야할 탄을 저장함
        for i in range(len(baseatack)):
            baseatack[i].update()
            delatack=0
            for j in range(len(bastion)): # 충돌체크를 통해서 주인공의 평타와 바스티온을 비교하여 hp를 감소시킵니다.
                if collide(bastion[j],baseatack[i]) and delatack==0:
                    bastion[j].HP_state(baseatack[i].get_damage())
                    basei.append(i)
                    delatack=1

            if collide(boss, baseatack[i]) and delatack==0 and boss.get_hp()>0:
                boss.HP_state(baseatack[i].get_damage())
                basei.append(i)
                delatack = 1

            if 1000<baseatack[i].get_y() and delatack==0:
                basei.append(i)
                delatack = 1


        if len(basei)>0: #탄이 멀리 나갔을때 지운다.
            basetemp=0
            for i in range(len(basei)):
                del baseatack[basei[i]-basetemp]
                basetemp+=1

        bastempi = [] #여기서 바스티온의 제거를 결정한다.
        for i in range(len(bastion)):
            if bastion[i].get_hp()<=0:
                bastempi.append(i)
        enemytemp = 0
        for i in range(len(bastempi)):
            del bastion[(bastempi[i])-enemytemp]
            ++enemytemp
        #여기까지 바스티온의 제거

        for i in range(len(bastion)): #바스티온의 주인공 인식
            bastion[i].update(mainhero.get_x,mainhero.get_x)
            dota=bastion_sence(bastion[i] , mainhero)
            bastion[i].sence_hero(dota)
            if dota==True:
                enemyatack.append(Enemybullet(bastion[i].get_x(), bastion[i].get_y() - 50))

        #여기서 부터 바스티온 기본탄환
        enemyi=[]
        for i in range(len(enemyatack)):
            delatack = 0
            enemyatack[i].update()
            if 200 > enemyatack[i].get_y() and delatack == 0:
                enemyi.append(i)
                delatack = 1
        if len(enemyi)>0: #탄이 멀리 나갔을때 지운다.
            Ebullettemp=0
            for i in range(len(enemyi)):
                del enemyatack[enemyi[i]-Ebullettemp]
                ++Ebullettemp
        #여기까지 바스티온 기본탄환


        if boss.get_hp() > 0:
            boss.update()



def draw(frame_time):
    global mainhero, baseatack
    global bastion,enemyatack
    global boss
    clear_canvas()
    mainhero.draw()


    for i in range(len(baseatack)):
        baseatack[i].draw()


    for i in range(len(bastion)):
        bastion[i].draw()
    if boss.get_hp()>0: boss.draw()

    for i in range(len(enemyatack)):
        enemyatack[i].draw()
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
                baseatack.append(bullet(mainhero.get_x(),mainhero.get_y()+50))
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