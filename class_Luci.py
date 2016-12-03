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
        self.image=load_image('luci_character.png')
        self.fireimage = load_image('fire.png')

        self.hpimage = load_image('hero_hp.png')
        self.emptyhpimage = load_image('hero_emptyhp.png')
        self.fireframe=0
        self.boost=10

    def transxy(self,xx,yy):
        self.x+=xx
        self.y+=yy


    def update(self,x_right, x_left, y_up, y_down):

        if self.hit>0:
            self.hit=(self.hit+1)%10

        self.frame=(self.frame+1)%8
        self.fireframe=(self.fireframe+1)%6

        if x_right == True and self.x <= 760:
            self.x = self.x + (self.speed+self.boost)
        if x_left == True and self.x >= 40:
            self.x = self.x - (self.speed+self.boost)
        if y_up == True and self.y < 960:
            self.y = self.y + (self.speed+self.boost)
        elif y_down == True and self.y > 40:
            self.y = self.y - (self.speed+self.boost)



    def draw(self):

        if self.hp > 0 and self.get_hit() % 2 == 0:
            self.image.clip_draw(self.frame * 80, 0, 80, 100, self.x, self.y)
            self.fireimage.clip_draw(self.fireframe * 27, 0, 27, 27, self.x, self.y+20)
        self.emptyhpimage.clip_draw(0, 0, 50, 200, 780, 700)
        self.hpimage.clip_draw(0, 0, 50, 200, 780, 700)

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