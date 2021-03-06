import random
import game_framework

from pico2d import*


class Luci:                   #메인캐릭터 자
    def __init__(self,xx,yy):
        self.frame=random.randint(0, 8)
        self.x=xx
        self.y=yy
        self.speed=20
        self.hp=500
        self.hit=0
        self.boostheal_count=0
        self.boostspeed_count=0
        self.boostheal = 0
        self.boostspeed = 0
        self.boost_charge = 0
        self.saveframe=0
        self.image=load_image('luci_character.png')
        self.backhealimage = load_image('backlight_heal.png')
        self.backspeedimage= load_image('backlight_speed.png')

        self.hpimage = load_image('hero_hp.png')
        self.mpimage = load_image('hero_mp.png')
        self.emptyhpimage = load_image('hero_emptyhp.png')

        self.healboostimage = load_image('hero_healboost.png')
        self.speedboostimage = load_image('hero_speedboost.png')

        self.fireframe=0
        self.boost=10

    def transxy(self,xx,yy):
        self.x+=xx
        self.y+=yy


    def update(self,nowframe,x_right, x_left, y_up, y_down):
        if self.hit>0:
            self.hit=(self.hit+int(nowframe))%10

        self.saveframe=self.saveframe+nowframe/4*3
        if int(self.saveframe):
            self.frame = (self.frame + 1) % 8
            self.saveframe=0
        self.fireframe=(self.fireframe+int(nowframe))%6

        if self.boost_charge>0:
            self.boost_charge=(self.boost_charge+1)
            if self.boost_charge>100: self.boost_charge=0

        if self.boostheal_count>0:
            self.hp=self.hp+self.boostheal
            if self.hp>500: self.hp=500

            self.boostheal_count=self.boostheal_count+1
            if self.boostheal_count==30:
                self.boostheal=0.5

        elif self.boostspeed_count>0:
            self.boostspeed_count=self.boostspeed_count+1
            if self.boostspeed_count==30:
                self.boostspeed=10




        if self.boostspeed_count>0:
            self.boostspeed_count=self.boostspeed_count+int(nowframe)



        if x_right == True and self.x <= 710:
            self.x = self.x + (self.speed+self.boostspeed)*nowframe
        if x_left == True and self.x >= 40:
            self.x = self.x - (self.speed+self.boostspeed)*nowframe
        if y_up == True and self.y < 960:
            self.y = self.y + (self.speed+self.boostspeed)*nowframe
        elif y_down == True and self.y > 40:
            self.y = self.y - (self.speed+self.boostspeed)*nowframe



    def draw(self):

        if self.boostheal_count:
            self.healboostimage.clip_draw(self.boostheal_count%3 * 100, 0, 100, 100, self.x, self.y-20)
        elif self.boostspeed_count:
            self.speedboostimage.clip_draw(self.boostspeed_count%3 * 100, 0, 100, 100, self.x, self.y-20)

        if self.hp > 0 and self.get_hit() % 2 == 0:
            self.image.clip_draw(self.frame * 80, 0, 80, 100, self.x, self.y)

        if self.boostheal_count:
            self.backhealimage.clip_draw(self.fireframe * 27, 0, 27, 27, self.x, self.y + 20)
        elif self.boostspeed_count:
            self.backspeedimage.clip_draw(self.fireframe * 27, 0, 27, 27, self.x, self.y + 20)

        self.emptyhpimage.clip_draw(0, 0, 50, 200, 780, 700)

        #hp
        hhh=(int)(2 * self.hp / 5)
        self.hpimage.clip_draw(0, 0, 50, hhh, 775, 700-(200-hhh)/2)

        #mp
        if self.boost_charge>0:
            mp=(int)(2 * self.boost_charge )
            self.mpimage.clip_draw(0, 0, 50, mp, 775, 400 - (200 - mp) / 2)
        else:
            self.mpimage.clip_draw(0, 0, 50, 200, 775, 400)

    def get_bb(self):
        return self.x-20,self.y-30,self.x+20,self.y+30
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

    def __init__(self,xx,yy):## 수정 및 폭탄
        self.x=xx
        self.y=yy
        self.speed=40
        self.damage=10
        self.image = load_image('soundwavecharge.png')


    def draw(self):

        self.image.clip_draw(0, 0, 50, 70, self.x, self.y)

    def update(self,nowframe):
        self.y=self.y+self.speed*nowframe
    def get_bb(self):
        return self.x-15,self.y-15,self.x+15,self.y+15
    def get_y(self):
        return self.y
    def get_damage(self):
        return self.damage
    def draw_bb(self):
        draw_rectangle(*self.get_bb())