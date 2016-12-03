import random
import json
import os


from pico2d import *

import game_framework

from class_enemy import Enemy,Enemybullet,Boss,Bossbullet,Enemy_second

from class_Luci import Luci,bullet


mainhero=None
total_frametime=None

x_right=x_left=y_up=y_down=None

boss=None

bastion=[]
enemyatack=[]
bosstan=[]

redline=None
wolrdy=None
wolrdspeed=None
map=None

#reinhardt=None






class Map:                 #지도
    def __init__(self):
        self.bgm = load_music('wave.mp3')
        self.bgm.set_volume(50)
        self.bgm.repeat_play()

        self.xone=400
        self.yone=1000
        self.xtwo = 400
        self.ytwo = 3000
        self.speed=40

        self.image = load_image('map_forest.png')

    def draw(self):
        if self.yone<2000:
            self.image.draw(self.xone, self.yone)
        if self.ytwo< 2000:
            self.image.draw(self.xtwo, self.ytwo)

    def update(self,worldspeed):
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
        global boss

        total_frametime = 0
        mainhero = Luci(300, 400)
        worldy = 0
        worldspeed = 10
        boss = Boss()
        x_right = x_left = y_up = y_down = False #키입력
        redline = False

        self.reinhardt=[]#라인하르트 초기화
        self.reinhardt.append(Enemy_second(200,700))


        self.heroatack=[]
        map = Map() #맵클래스 생성

    def draw(self,fram_time):
        global mainhero, redline, worldy
        global bastion, enemyatack
        global boss
        clear_canvas()

        map.draw()

        mainhero.draw()



        for i in range(len(self.heroatack)):
            self.heroatack[i].draw()

        for i in range(len(bastion)):
            bastion[i].draw()

        for i in range(len(self.reinhardt)):
            self.reinhardt[i].draw()


        if worldy > 7000: #보스전
            if boss.hp > 0:
                boss.draw()
                for i in range(len(bosstan)):
                    bosstan[i].draw()

        for i in range(len(enemyatack)):
            enemyatack[i].draw()

        if redline:
            if mainhero.hp > 0 and mainhero.get_hit() % 2 == 0:
                mainhero.draw_bb()

            for i in range(len(self.heroatack)):
                self.heroatack[i].draw_bb()

            for i in range(len(bastion)):
                bastion[i].draw_bb()

            for i in range(len(self.reinhardt)):
                self.reinhardt[i].draw_bb()

            if worldy > 7000:
                if boss.hp > 0:
                    boss.draw_bb()
                    for i in range(len(bosstan)):
                        bosstan[i].draw_bb()

            for i in range(len(enemyatack)):
                enemyatack[i].draw_bb()




        update_canvas()

    def update(self,frame_time):
        global mainhero, worldy, worldspeed, map
        global x_right, x_left, y_up, y_down
        global total_frametime
        global bastion, enemyatack
        global boss

        total_frametime += frame_time

        if total_frametime > 0.1:
            total_frametime = 0
            mainhero.update(x_right, x_left, y_up, y_down)

            worldy = worldy + worldspeed

            if worldy:  #여기가 생산라인
                if worldy % 200 == 0 and worldy < 5500:
                    for i in range(random.randint(1, 2)):
                        randtemp=random.randint(1, 2)
                        if randtemp==1 :
                            bastion.append(Enemy(random.randint(1, 7) * 100, 1150))
                        elif randtemp==2 :
                            self.reinhardt.append(Enemy_second(random.randint(1, 6) * 120, 1150))

                elif worldy > 8500 and worldy % 900 == 0:
                    for i in range(1, 6):
                        bastion.append(Enemy(i * 130, boss.y))



            del_heroatack = []  # 지워야할 탄을 저장함

            for i in range(len(self.heroatack)):  # 주인공의 탄환 발사
                self.heroatack[i].update()

                touching_heroatack = 0 #touching_heroatack는 탄이 접촉을 했는지 체크한다. 터치했을경우 값을 가지게 된다.

                for j in range(len(bastion)):  # 충돌체크를 통해서 주인공의 평타와 바스티온을 비교하여 hp를 감소시킵니다.
                    if self.collide(bastion[j], self.heroatack[i]) and touching_heroatack == 0:
                        bastion[j].HP_state(self.heroatack[i].get_damage())
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
                        del_heroatack.append(i)
                        touching_heroatack = 1

                if worldy > 7000: #보스전 돌입을 말한다. 나중에 추가로 해준다.
                    if self.collide(boss, self.heroatack[i]) and touching_heroatack == 0 and boss.hp > 0:
                        boss.HP_state(self.heroatack[i].get_damage())
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
                    deadsine = 1
                if bastion[i].y < -50 and deadsine == 0:
                    print(bastion[i].y)
                    del_bastion.append(i)
                    deadsine = 1

            enemytemp = 0
            for i in range(len(del_bastion)):
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
                if self.reinhardt[i].y < -120 and deadsine == 0:
                    print('55')
                    del_reinhardt.append(i)
                    deadsine = 1

            enemytemp = 0
            for i in range(len(del_reinhardt)):
                del self.reinhardt[(del_reinhardt[i]) - enemytemp]
                enemytemp = enemytemp + 1
             # 라인하르트 제거 완료


#1111111111111111111111111111111111111111111111111111111111111111111111111111111111111

            for i in range(len(bastion)):  # 바스티온 업데이트 및 주인공 인식
                bastion[i].update(worldspeed/2)
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
                enemyatack[i].update(worldspeed)
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
                self.reinhardt[i].update(worldspeed/2)
                sencecheck = self.reinhardt[i].reinhardt_sence(mainhero)
                if sencecheck == True and self.reinhardt[i].atacktime==0:
                    print('sss')
                    self.reinhardt[i].state=2
                    self.reinhardt[i].atacktime=1
                    self.reinhardt[i].frame=0
                    #enemyatack.append(Enemybullet(self.reinhardt[i].x, self.reinhardt[i].y - 50))
                if self.reinhardt[i].state==2 and self.reinhardt[i].atacktime>10:
                    if  self.collide_fire(mainhero,self.reinhardt[i].x,self.reinhardt[i].y-100):
                        print('32')
                        mainhero.HP_state(self.reinhardt[i].damage)
                    if  self.collide_fire(mainhero,self.reinhardt[i].x,self.reinhardt[i].y-200):
                        print('32')
                        mainhero.HP_state(self.reinhardt[i].damage)
                    if  self.collide_fire(mainhero,self.reinhardt[i].x-100,self.reinhardt[i].y-200):
                        print('32')
                        mainhero.HP_state(self.reinhardt[i].damage)
                    if  self.collide_fire(mainhero,self.reinhardt[i].x+100,self.reinhardt[i].y-200):
                        print('32')
                        mainhero.HP_state(self.reinhardt[i].damage)
            #업데이트 완료


            if worldy > 7000: #보스등장
                if boss.hp > 0:
                    boss.update()
                    if boss.get_tanframe() == 1:
                        bosstan.append(Bossbullet(boss.x - 100, boss.y, mainhero.x, mainhero.y))

                    if boss.get_tanframe() == 5:
                        bosstan.append(Bossbullet(boss.x + 100, boss.y, mainhero.x, mainhero.y))

                    bossi = []
                    for i in range(len(bosstan)):
                        bosstan[i].update()
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





            map.update(worldspeed)

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

        return True

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

