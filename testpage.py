import random
import json
import os


from pico2d import *
import game_framework

from class_enemy import Enemy,Enemybullet,Boss,Bossbullet


mainhero=None
total_frametime=None
x_right=x_left=y_up=y_down=None

boss=None

bastion=[]
baseatack=[]
enemyatack=[]
bosstan=[]

redline=None
wolrdy=None
wolrdspeed=None

map=None

class Luci:                   #메인캐릭터 자
    def __init__(self,xx,yy):
        self.frame=random.randint(0, 8)
        self.x=xx
        self.y=yy
        self.speed=20
        self.hp=500
        self.hit=0
        self.image=load_image('luci_character.png')
        self.fireimage = load_image('fire.png')
        self.fireframe=0

    def transxy(self,xx,yy):
        self.x+=xx
        self.y+=yy


    def update(self):
        global x_right, x_left, y_up, y_down

        if self.hit>0:
            self.hit=(self.hit+1)%10

        self.frame=(self.frame+1)%8
        self.fireframe=(self.fireframe+1)%6

        if x_right == True and self.x <= 760:
            self.x = self.x + self.speed
        if x_left == True and self.x >= 40:
            self.x = self.x - self.speed
        if y_up == True and self.y < 960:
            self.y = self.y + self.speed
        elif y_down == True and self.y > 40:
            self.y = self.y - self.speed



    def draw(self):
        self.image.clip_draw(self.frame * 80, 0, 80, 100, self.x, self.y)
        self.fireimage.clip_draw(self.fireframe * 27, 0, 27, 27, self.x, self.y+20)
    def get_bb(self):
        return self.x-40,self.y-40,self.x+50,self.y+50
    def get_aa(self):
        return self.x, self.y
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def HP_state(self,a):
        if a>0 and self.hit==0:
            self.hp = self.hp - a
            self.hit=1
    def get_hp(self):
        return self.hp
    def get_hit(self):
        return self.hit
    def draw_bb(self):
        draw_rectangle(*self.get_bb())



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
    def draw_bb(self):
        draw_rectangle(*self.get_bb())


class Map:                 #지도

    def __init__(self):
        self.bgm = load_music('wave.mp3')
        self.bgm.set_volume(50)
        self.bgm.repeat_play()

        self.xone=400
        self.yone=1000
        self.xtwo = 400
        self.ytwo = 3000
        self.speed=50

        self.image = load_image('map.png')

    def draw(self):
        if self.yone<2000:
            self.image.draw(self.xone, self.yone)
        if self.ytwo< 2000:
            self.image.draw(self.xtwo, self.ytwo)

    def update(self):
        self.yone=self.yone-self.speed
        self.ytwo=self.ytwo-self.speed
        if self.yone<=-1000:
            self.yone=3000
        if self.ytwo<=-1000:
            self.ytwo=3000






def enter():
    global mainhero,total_frametime,redline,worldy,worldspeed,map
    global x_right,x_left,y_up,y_down #키의 상태값
    global bastion
    global boss
    total_frametime=0
    mainhero=Luci(300,400)
    worldy=0
    worldspeed=10
    boss=Boss()
    x_right = x_left = y_up = y_down=False
    redline = False
    map=Map()
def exit():
    global mainhero,map
    del(mainhero)

def update(frame_time):
    global mainhero, baseatack,worldy,worldspeed,map
    global total_frametime
    global bastion,enemyatack
    global boss




    total_frametime+= frame_time


    if total_frametime>0.1:
        total_frametime=0
        mainhero.update()
        worldy=worldy+ worldspeed

        if worldy:
            if worldy%100==0 and worldy<6500:
                for i in range(random.randint(1, 3)):
                    bastion.append(Enemy(random.randint(1, 7)*100, 1150))
            elif worldy>8500 and worldy%900==0:
                for i in range(1,6):
                    bastion.append(Enemy(i * 130, boss.get_y()))

        basei=[]#지워야할 탄을 저장함
        for i in range(len(baseatack)): # 주인공의 탄환 발사
            baseatack[i].update()
            delatack=0
            for j in range(len(bastion)): # 충돌체크를 통해서 주인공의 평타와 바스티온을 비교하여 hp를 감소시킵니다.
                if collide(bastion[j],baseatack[i]) and delatack==0:
                    bastion[j].HP_state(baseatack[i].get_damage())
                    basei.append(i)
                    delatack=1
            if worldy>7000:
                if collide(boss, baseatack[i]) and delatack==0 and boss.get_hp()>0:
                    boss.HP_state(baseatack[i].get_damage())
                    basei.append(i)
                    delatack = 1

            if 1000<baseatack[i].get_y() and delatack==0:
                basei.append(i)
                delatack = 1

        if len(basei)>0: #주인공 탄이 멀리 나갔을때 지운다.
            basetemp=0
            for i in range(len(basei)):
                del baseatack[basei[i]-basetemp]
                basetemp+=1


        bastempi = [] #여기서 바스티온의 제거를 결정한다.
        for i in range(len(bastion)):
            deadsine=0
            if bastion[i].get_hp()<=0 and deadsine==0:
                bastempi.append(i)
                deadsine=1
            if bastion[i].get_y()<-50 and deadsine==0:
                print(bastion[i].get_y())
                bastempi.append(i)
                deadsine=1

        enemytemp = 0
        for i in range(len(bastempi)):
            del bastion[(bastempi[i])-enemytemp]
            enemytemp=enemytemp+1

        #여기까지 바스티온의 제거

        for i in range(len(bastion)): #바스티온의 주인공 인식
            bastion[i].update(mainhero.get_x,mainhero.get_x)
            dota=bastion_sence(bastion[i] , mainhero)
            bastion[i].sence_hero(dota)
            check=bastion[i].get_bulletcount()
            if dota==True and check==True:
                enemyatack.append(Enemybullet(bastion[i].get_x(), bastion[i].get_y() - 50))
                bastion[i].up_bulletcount()

        #여기서 부터 바스티온 기본탄환
        enemyi=[]
        for i in range(len(enemyatack)):
            enemyatack[i].update()
            delatack = 0
            if collide(mainhero, enemyatack[i]) and delatack == 0 and mainhero.get_hp() > 0: #주인공 피격 후 hp감소
                mainhero.HP_state(enemyatack[i].get_damage())
                enemyi.append(i)
                delatack = 1
            if -50 > enemyatack[i].get_y() and delatack == 0: #화면밖으로 나간 총알
                enemyi.append(i)
                delatack = 1
        if len(enemyi)>0: #탄이 멀리 나갔을때 지운다.
            Ebullettemp=0
            for i in range(len(enemyi)):
                del enemyatack[enemyi[i]-Ebullettemp]
                Ebullettemp=Ebullettemp+1
        #여기까지 바스티온 기본탄환
        if worldy>7000:
            if boss.get_hp() > 0:
                boss.update()
                if boss.get_tanframe() == 1:
                    bosstan.append(Bossbullet(boss.get_x() - 100, boss.get_y(), mainhero.get_x(), mainhero.get_y()))

                if boss.get_tanframe() == 5:
                    bosstan.append(Bossbullet(boss.get_x() + 100, boss.get_y(), mainhero.get_x(), mainhero.get_y()))

                bossi = []
                for i in range(len(bosstan)):
                    bosstan[i].update()
                    delatack = 0

                    if collide(mainhero, bosstan[i]) and delatack == 0 and mainhero.get_hp() > 0:
                        mainhero.HP_state(bosstan[i].get_damage())
                        enemyi.append(i)
                        delatack = 1
                    elif -50 > bosstan[i].get_y() and delatack == 0:  # 화면밖으로 나간 총알
                        bossi.append(i)
                        delatack = 1
                    elif 1000 < bosstan[i].get_y() and delatack == 0:
                        bossi.append(i)
                        delatack = 1
                    elif 800 < bosstan[i].get_x() and delatack == 0:
                        bossi.append(i)
                        delatack = 1
                    elif 0 > bosstan[i].get_x() and delatack == 0:
                        bossi.append(i)
                        delatack = 1

                if len(bossi) > 0:  # 탄이 멀리 나갔을때 지운다.
                    Bbullettemp = 0
                    for i in range(len(bossi)):
                        del bosstan[bossi[i] - Bbullettemp]
                        Bbullettemp = Bbullettemp + 1

            if collide(mainhero, boss):
                mainhero.HP_state(boss.get_damage())
        map.update()


def draw(frame_time):
    global mainhero, baseatack,redline,worldy
    global bastion,enemyatack
    global boss
    clear_canvas()

    map.draw()
    if mainhero.get_hp()>0 and mainhero.get_hit()%2==0:
        mainhero.draw()


    for i in range(len(baseatack)):
        baseatack[i].draw()


    for i in range(len(bastion)):
        bastion[i].draw()

    if worldy>7000:
        if boss.get_hp() > 0:
            boss.draw()
            for i in range(len(bosstan)):
                bosstan[i].draw()

    for i in range(len(enemyatack)):
        enemyatack[i].draw()


    if redline:
        if mainhero.get_hp() > 0 and mainhero.get_hit() % 2 == 0:
            mainhero.draw_bb()

        for i in range(len(baseatack)):
            baseatack[i].draw_bb()

        for i in range(len(bastion)):
            bastion[i].draw_bb()
        if worldy > 7000:
            if boss.get_hp() > 0:
                boss.draw_bb()
                for i in range(len(bosstan)):
                    bosstan[i].draw_bb()

        for i in range(len(enemyatack)):
            enemyatack[i].draw_bb()

    update_canvas()



def handle_events(frame_time):
    global x_right, x_left, y_up, y_down,redline
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
            if event.key == SDLK_1:
                if redline: redline=False
                else:  redline=True
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
    if bottom_a<y : return False
    if bottom_a-y<200: return False
    return True