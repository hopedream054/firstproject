import random
import json
import os
import worldtwo

from pico2d import *

import game_framework

from class_enemy import Enemy,Enemybullet,Boss,Bossbullet,Enemy_second,Enemy_third,Genji_shot,Genji_shadow
from class_Luci import Luci,bullet
from class_item import Item_Battery
from class_sound import Sound
mainhero=None
total_frametime=None

x_right=x_left=y_up=y_down=None

boss=None


enemyatack=[]
bosstan=[]

redline=None
wolrdy=None
map=None

blackimage=None




class Map:                 #지도
    def __init__(self):





        self.xone=400
        self.yone=1000
        self.xtwo = 400
        self.ytwo = 3000
        self.speed=10

        self.image = load_image('map_desert.png')

    def draw(self):
        if self.yone<2000:
            self.image.draw(self.xone, self.yone)
        if self.ytwo< 2000:
            self.image.draw(self.xtwo, self.ytwo)

    def update(self,nowframe,worldspeed):
        self.yone=self.yone-self.speed-worldspeed
        self.ytwo=self.ytwo-self.speed-worldspeed
        if self.yone<=-1000:
            self.yone=3000
        if self.ytwo<=-1000:
            self.ytwo=3000



class worldclass:
    def __init__(self):
        global mainhero, total_frametime, redline, worldy, worldspeed, map
        global x_right, x_left, y_up, y_down  # 키의 상태값
        global bastion
        global boss,blackimage

        self.bgm = load_music('stageonebgm.mp3')
        self.bgm.set_volume(49)
        self.bgm.repeat_play()

        bastion = []
        total_frametime = 0
        mainhero = Luci(300, 400)
        worldy = 0
        worldspeed = 10
        boss = Boss()
        x_right = x_left = y_up = y_down = False #키입력
        redline = False
        self.restart=0
        self.reinhardt=[]#라인하르트 초기화
        self.reinhardt.append(Enemy_second(200,700))

        self.genji = []  # 겐지 초기화
        self.genji.append(Enemy_third(700, 700))
        self.genji_atack=[]
        self.genji_shadow = []

        self.stage=0
        self.war=0

        blackimage= load_image('black.png')
        self. hitimage = load_image('hit_effect.png')
        self.image_ending = load_image('endiing.png')
        self.warningimage=load_image('warning.png')
        self.battery = []
        self.battery.append(Item_Battery(500, 700))

        self.hitx=[]
        self.hity=[]
        self.hitn=0

        self.heroatack=[]
        map = Map() #맵클래스 생성
        self.sound=Sound()
        wolrdy=0
        bosstan = []

    def draw(self,fram_time):
        global mainhero, redline, worldy
        global bastion, enemyatack
        global boss,blackimage
        clear_canvas()

        map.draw()



        if self.stage==0 and mainhero.hp>0:
            for i in range(len(self.heroatack)):
                self.heroatack[i].draw()

            for i in range(len(bastion)):
                bastion[i].draw()

            for i in range(len(self.reinhardt)):
                self.reinhardt[i].draw()

            for i in range(len(self.genji)):
                self.genji[i].draw()

            if worldy>7800 and worldy <8400:

                self.warningimage.clip_draw(0, 0, 800, 300, 400, 700)
            elif worldy > 8500:  # 보스전
                if boss.hp > 0:
                    boss.draw()
                    for i in range(len(bosstan)):
                        bosstan[i].draw()

            for i in range(len(enemyatack)):
                enemyatack[i].draw()

            for i in range(len(self.genji_atack)):
                self.genji_atack[i].draw()

            for i in range(len(self.genji_shadow)):
                self.genji_shadow[i].draw()

            for i in range(len(self.battery)):
                self.battery[i].draw()

            for i in range(self.hitn):
                self.hitimage.draw(self.hitx[i], self.hity[i])

            blackimage.draw(775, 500)
            mainhero.draw()

            if redline:
                if mainhero.hp > 0 and mainhero.get_hit() % 2 == 0:
                    mainhero.draw_bb()

                for i in range(len(self.heroatack)):
                    self.heroatack[i].draw_bb()

                for i in range(len(bastion)):
                    bastion[i].draw_bb()

                for i in range(len(self.reinhardt)):
                    self.reinhardt[i].draw_bb()

                for i in range(len(self.genji)):
                    self.genji[i].draw_bb()
                for i in range(len(self.genji_shadow)):
                    self.genji_shadow[i].draw_bb()
                if worldy > 8500:
                    if boss.hp > 0:
                        boss.draw_bb()
                        for i in range(len(bosstan)):
                            bosstan[i].draw_bb()

                for i in range(len(enemyatack)):
                    enemyatack[i].draw_bb()
                for i in range(len(self.genji_atack)):
                    self.genji_atack[i].draw_bb()
        elif self.stage == 1:
            self.image_ending.draw(400, 500)


        update_canvas()

    def update(self,frame_time):
        global mainhero, worldy, worldspeed, map
        global x_right, x_left, y_up, y_down
        global total_frametime
        global bastion, enemyatack
        global boss

        total_frametime += frame_time




        if boss.hp<=0:
            self.stage=1
        elif mainhero.hp <= 0:
            self.restart=1
            for i in range(len(bastion)):
                del bastion[0]
        elif total_frametime > 0.05:
            nowframe=total_frametime*20
            total_frametime = 0
            mainhero.update(nowframe,x_right, x_left, y_up, y_down)

            worldy = worldy + worldspeed


            for i in range(self.hitn):
                print(self.hitn)
                print(i)
                del self.hitx[0]
                del self.hity[0]
            self.hitn=0

            if worldy:  #여기가 생산라인
                if worldy % 300 == 0 and worldy < 7000:
                    for i in range(random.randint(1, 2)):
                        randtemp=random.randint(0, 5)
                        if randtemp>0 and   randtemp<4:
                            bastion.append(Enemy(random.randint(1, 7) * 100, 1050))
                        elif randtemp==4 :
                            self.reinhardt.append(Enemy_second(random.randint(1, 6) * 120, 1060))
                        elif randtemp==5 :
                            self.genji.append(Enemy_third(random.randint(3, 6) * 100, 1050))
                elif worldy>7800 and self.war==0:
                    self.sound.warningsound.play()
                    self.war=1
                elif worldy > 10500 and worldy % 900 == 0:
                    for i in range(1, 6):
                        bastion.append(Enemy(i * 130, boss.y))



            del_heroatack = []  # 지워야할 탄을 저장함

            for i in range(len(self.heroatack)):  # 주인공의 탄환 발사
                self.heroatack[i].update(nowframe)

                touching_heroatack = 0 #touching_heroatack는 탄이 접촉을 했는지 체크한다. 터치했을경우 값을 가지게 된다.

                for j in range(len(bastion)):  # 충돌체크를 통해서 주인공의 평타와 바스티온을 비교하여 hp를 감소시킵니다.
                    if self.collide(bastion[j], self.heroatack[i]) and touching_heroatack == 0:
                        bastion[j].HP_state(self.heroatack[i].get_damage())
                        self.hitx.append(self.heroatack[i].x)
                        self.hity.append(self.heroatack[i].y)
                        self.hitn = self.hitn + 1
                        del_heroatack.append(i)

                        touching_heroatack = 1

                for j in range(len(self.reinhardt)):  # 충돌체크를 통해서 주인공의 평타와 라인하르트를 비교하여 hp를 감소시킵니다.
                    if self.collide(self.reinhardt[j], self.heroatack[i]) and touching_heroatack == 0:
                        if self.reinhardt[j].state == 3 and self.reinhardt[j].shild_hp > 0:
                            self.reinhardt[j].frame=0
                            self.reinhardt[j].shild_hp = self.reinhardt[j].shild_hp - self.heroatack[i].damage
                            if self.reinhardt[j].shild_hp<=0: self.reinhardt[j].state=1 #실드가 깨질경우임 추후 수정가능

                        else:
                            self.reinhardt[j].hp = self.reinhardt[j].hp - self.heroatack[i].damage
                        self.hitx.append(self.heroatack[i].x)
                        self.hity.append(self.heroatack[i].y)
                        self.hitn = self.hitn + 1
                        del_heroatack.append(i)
                        touching_heroatack = 1

                for j in range(len(self.genji)):  # 충돌체크를 통해서 주인공의 평타와 바스티온을 비교하여 hp를 감소시킵니다.
                    if self.collide(self.genji[j], self.heroatack[i]) and touching_heroatack == 0:
                        self.genji[j].hp = self.genji[j].hp - self.heroatack[i].damage
                        self.hitx.append(self.heroatack[i].x)
                        self.hity.append(self.heroatack[i].y)
                        self.hitn = self.hitn + 1
                        del_heroatack.append(i)

                        touching_heroatack = 1
                if touching_heroatack==1:
                    self.sound.hero_atacksound.play()



                if worldy > 8500: #보스전 돌입을 말한다. 나중에 추가로 해준다.
                    if self.collide(boss, self.heroatack[i]) and touching_heroatack == 0 and boss.hp > 0:
                        boss.HP_state(self.heroatack[i].get_damage())
                        self.hitx.append(self.heroatack[i].x)
                        self.hity.append(self.heroatack[i].y)
                        self.hitn = self.hitn + 1
                        del_heroatack.append(i)
                        touching_heroatack = 1

                if 1000 < self.heroatack[i].y and touching_heroatack == 0:
                    del_heroatack.append(i)
                    touching_heroatack = 1

            if len(del_heroatack) > 0:  # 주인공 탄이 멀리 나갔을때 지운다.
                basetemp = 0
                for i in range(len(del_heroatack)):
                    del self.heroatack[del_heroatack[i] - basetemp]
                    basetemp += 1

##11111111111111111111111111111111111111111111111111111111111111111111111111111111111

            # 여기서 바스티온의 제거를 결정한다.
            del_bastion = []
            for i in range(len(bastion)):
                deadsine = 0
                if bastion[i].hp <= 0 and deadsine == 0:
                    del_bastion.append(i)
                    self.sound.bastion_dead.play()
                    deadsine = 1
                if bastion[i].y < -50 and deadsine == 0:
                    print(bastion[i].y)
                    del_bastion.append(i)
                    deadsine = 1

            enemytemp = 0
            for i in range(len(del_bastion)):
                #item 랜덤 생성
                if random.randint(1, 3)==3: self.battery.append(Item_Battery(bastion[(del_bastion[i]) - enemytemp].x, bastion[(del_bastion[i]) - enemytemp].y))

                del bastion[(del_bastion[i]) - enemytemp]
                enemytemp = enemytemp + 1
            # 여기까지 바스티온의 제거


            #라인하르트 제거.
            del_reinhardt = []
            for i in range(len(self.reinhardt)):
                deadsine = 0
                if self.reinhardt[i].hp <= 0 and deadsine == 0:
                    print('50')
                    del_reinhardt.append(i)
                    deadsine = 1
                    self.sound.reinhartd_dead.play()
                if self.reinhardt[i].y < -120 and deadsine == 0:
                    print('55')
                    del_reinhardt.append(i)
                    deadsine = 1

            enemytemp = 0
            for i in range(len(del_reinhardt)):
                del self.reinhardt[(del_reinhardt[i]) - enemytemp]
                enemytemp = enemytemp + 1
             # 라인하르트 제거 완료


            # 겐지 제거.
            del_genji = []
            for i in range(len(self.genji)):
                deadsine = 0
                if self.genji[i].hp <= 0 and deadsine == 0:
                    print('50')
                    del_genji.append(i)
                    deadsine = 1
                    self.sound.genji_dead.play()
                elif self.genji[i].y < -120 and deadsine == 0:
                    del_genji.append(i)
                    deadsine = 1
                elif self.genji[i].x < -60 and deadsine == 0:
                    del_genji.append(i)
                    deadsine = 1
                elif self.genji[i].x > 860 and deadsine == 0:
                    del_genji.append(i)
                    deadsine = 1

            enemytemp = 0
            for i in range(len(del_genji)):
                print('1')
                del self.genji[(del_genji[i]) - enemytemp]
                enemytemp = enemytemp + 1
            # 겐지 제거 완료

#1111111111111111111111111111111111111111111111111111111111111111111111111111111111111

            for i in range(len(bastion)):  # 바스티온 업데이트 및 주인공 인식
                bastion[i].update(nowframe,worldspeed/2)
                sencecheck = bastion[i].bastion_sence(mainhero)
                bastion[i].sence_hero(sencecheck)
                check = bastion[i].get_bulletcount()
                if sencecheck == True and check == True:
                    enemyatack.append(Enemybullet(bastion[i].x, bastion[i].y - 50))
                    bastion[i].up_bulletcount()
            #인식 및 업데이트 완료

            #바스티온 기본탄환 업데이트
            enemyi = []
            for i in range(len(enemyatack)):
                enemyatack[i].update(nowframe,worldspeed)
                delatack = 0

                if self.collide(mainhero, enemyatack[i]) and delatack == 0 and mainhero.hp > 0:  # 주인공 피격 후 hp감소
                    mainhero.HP_state(enemyatack[i].get_damage())
                    enemyi.append(i)
                    delatack = 1
                if -50 > enemyatack[i].y and delatack == 0:  # 화면밖으로 나간 총알
                    enemyi.append(i)
                    delatack = 1
            if len(enemyi) > 0:  # 탄이 멀리 나갔을때 지운다.
                Ebullettemp = 0
                for i in range(len(enemyi)):
                    del enemyatack[enemyi[i] - Ebullettemp]
                    Ebullettemp = Ebullettemp + 1
            # 업데이트 완료


            #라인하르트 업데이트
            for i in range(len(self.reinhardt)):
                self.reinhardt[i].update(nowframe,worldspeed/2)
                sencecheck = self.reinhardt[i].reinhardt_sence(mainhero)
                if sencecheck == True and self.reinhardt[i].atacktime==0:
                    self.reinhardt[i].state=2
                    self.reinhardt[i].atacktime=1
                    self.reinhardt[i].frame=0
                    #enemyatack.append(Enemybullet(self.reinhardt[i].x, self.reinhardt[i].y - 50))
                if self.reinhardt[i].state==2 and self.reinhardt[i].atacktime>10:
                    if  self.collide_fire(mainhero,self.reinhardt[i].x,self.reinhardt[i].y-100):
                        mainhero.HP_state(self.reinhardt[i].damage)
                    if  self.collide_fire(mainhero,self.reinhardt[i].x,self.reinhardt[i].y-200):
                        mainhero.HP_state(self.reinhardt[i].damage)
                    if  self.collide_fire(mainhero,self.reinhardt[i].x-100,self.reinhardt[i].y-200):
                        mainhero.HP_state(self.reinhardt[i].damage)
                    if  self.collide_fire(mainhero,self.reinhardt[i].x+100,self.reinhardt[i].y-200):
                        mainhero.HP_state(self.reinhardt[i].damage)
            #업데이트 완료


            #겐지 업데이트
            for i in range(len(self.genji)):  # 바스티온 업데이트 및 주인공 인식
                self.genji[i].update(nowframe,worldspeed/2)
                if self.genji[i].frame%5==0 and self.genji[i].state==1:
                    self.genji_atack.append(Genji_shot( self.genji[i].x,  self.genji[i].y - 50,0))
                    self.genji_atack.append(Genji_shot( self.genji[i].x,  self.genji[i].y - 50,10))
                    self.genji_atack.append(Genji_shot( self.genji[i].x,  self.genji[i].y - 50,-10))
                elif self.genji[i].frame % 2 == 1 and self.genji[i].state == 2:
                    self.genji_shadow.append(Genji_shadow(self.genji[i].x ,self.genji[i].y,(int)(self.genji[i].frame/2)))
            # 업데이트 완료

            # 겐지의 표창 업데이트
            enemyi = []

            for i in range(len(self.genji_atack)):
                self.genji_atack[i].update(nowframe,worldspeed)
                delatack = 0

                if self.collide(mainhero, self.genji_atack[i]) and delatack == 0 and mainhero.hp > 0:  # 주인공 피격 후 hp감소
                    mainhero.HP_state(self.genji_atack[i].get_damage())
                    enemyi.append(i)
                    delatack = 1
                if -50 > self.genji_atack[i].y and delatack == 0:  # 화면밖으로 나간 총알
                    enemyi.append(i)
                    delatack = 1
            if len(enemyi) > 0:  # 탄이 멀리 나갔을때 지운다.
                Ebullettemp = 0
                for i in range(len(enemyi)):
                    del self.genji_atack[enemyi[i] - Ebullettemp]
                    Ebullettemp = Ebullettemp + 1
            # 업데이트 완료

            enemyi = []
            # 겐지의 그림자 분신 업데이트
            for i in range(len(self.genji_shadow)):
                self.genji_shadow[i].update(nowframe,worldspeed)
                delatack = 0

                if self.collide(mainhero, self.genji_shadow[i]) and delatack == 0 and mainhero.hp > 0:  # 주인공 피격 후 hp감소
                    mainhero.HP_state(self.genji_shadow[i].damage)
                    enemyi.append(i)
                    delatack = 1
                if self.genji_shadow[i].frame>20 and delatack == 0:  # 화면밖으로 나간 총알
                    enemyi.append(i)
                    delatack = 1
            if len(enemyi) > 0: #제거한다
                Ebullettemp = 0
                for i in range(len(enemyi)):
                    print('10')
                    del self.genji_shadow[enemyi[i] - Ebullettemp]
                    Ebullettemp = Ebullettemp + 1
            #업데이트완료


            enemyi = []#아이템 업데이트
            for i in range(len(self.battery)):
                self.battery[i].update(nowframe,worldspeed)
                delatack = 0

                if self.collide(mainhero, self.battery[i]) and delatack == 0 and mainhero.boost_charge != 100:  #
                    mainhero.boost_charge=0
                    enemyi.append(i)
                    self.sound.item_get.play()
                    delatack = 1
                if self.battery[i].rotation==3 and delatack == 0:  #
                    enemyi.append(i)
                    delatack = 1
            if len(enemyi) > 0: #제거한다
                Ebullettemp = 0
                for i in range(len(enemyi)):
                    print('10')
                    del self.battery[enemyi[i] - Ebullettemp]
                    Ebullettemp = Ebullettemp + 1
            #업데이트 완료

            if worldy > 8500: #보스등장
                if boss.hp > 0:
                    boss.update(nowframe)
                    if boss.get_tanframe() == 1:
                        self.sound.bastion_dead.play()
                        bosstan.append(Bossbullet(boss.x - 100, boss.y, mainhero.x, mainhero.y))

                    if boss.get_tanframe() == 5:
                        self.sound.bastion_dead.play()
                        bosstan.append(Bossbullet(boss.x + 100, boss.y, mainhero.x, mainhero.y))

                    bossi = []
                    for i in range(len(bosstan)):
                        bosstan[i].update(nowframe)
                        delatack = 0

                        if self.collide(mainhero, bosstan[i]) and delatack == 0 and mainhero.hp > 0:
                            mainhero.HP_state(bosstan[i].get_damage())
                            enemyi.append(i)
                            delatack = 1
                        elif -50 > bosstan[i].y and delatack == 0:  # 화면밖으로 나간 총알
                            bossi.append(i)
                            delatack = 1
                        elif 1000 < bosstan[i].y and delatack == 0:
                            bossi.append(i)
                            delatack = 1
                        elif 800 < bosstan[i].x and delatack == 0:
                            bossi.append(i)
                            delatack = 1
                        elif 0 > bosstan[i].x and delatack == 0:
                            bossi.append(i)
                            delatack = 1

                    if len(bossi) > 0:  # 탄이 멀리 나갔을때 지운다.
                        Bbullettemp = 0
                        for i in range(len(bossi)):
                            print('1212')
                            del bosstan[bossi[i] - Bbullettemp]
                            Bbullettemp = Bbullettemp + 1

                if self.collide(mainhero, boss):
                    mainhero.HP_state(boss.get_damage())


            map.update(nowframe,worldspeed)

    def handle_events(self,frame_time):
        global x_right, x_left, y_up, y_down, redline
        global mainhero
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
                    self.heroatack.append(bullet(mainhero.x, mainhero.y + 50))
                if event.key == SDLK_z and mainhero.boost_charge==0:
                    print('z')
                    mainhero.boost_charge=1
                    mainhero.boostheal_count=1
                    mainhero.boostspeed_count = 0
                    mainhero.boostheal = 4
                    mainhero.boostspeed = 0
                elif event.key == SDLK_x and mainhero.boost_charge==0:
                    print('x')
                    mainhero.boost_charge = 1
                    mainhero.boostheal_count = 0
                    mainhero.boostspeed_count = 1
                    mainhero.boostheal = 0
                    mainhero.boostspeed = 25

                if event.key == SDLK_1:
                    if redline:
                        redline = False
                    else:
                        redline = True
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT:
                    x_right = False
                elif event.key == SDLK_LEFT:
                    x_left = False
                elif event.key == SDLK_UP:
                    y_up = False
                elif event.key == SDLK_DOWN:
                    y_down = False

    def collide(self,a, b):  # a:anemy b:tan
        left_a, bottom_a, right_a, top_a = a.get_bb()
        left_b, bottom_b, right_b, top_b = b.get_bb()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True#충돌

    def collide_fire(self,b,xx,yy):  # 불꽃파티클 충돌체크
        left_a=xx-50
        bottom_a=yy-50
        right_a=xx+50
        top_a =yy+50
        left_b, bottom_b, right_b, top_b = b.get_bb()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True