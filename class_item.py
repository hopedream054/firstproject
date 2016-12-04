import game_framework
import math
import random
from pico2d import*

class Item_Battery:                        #적3 겐지
    def __init__(self,xx,yy):
        self.x=xx
        self.y=yy
        self.dirx=1
        self.diry=1
        self.speedx=20
        self.speedy=20
        self.frame=0
        self.rotation=0
        self.image = load_image('itembattery.png')

    def draw(self):
        self.image.clip_draw(self.frame*30, 0, 30, 50, self.x, self.y)
    def update(self,worldspeed):
        if self.x>730:
            self.dirx=-1
        elif self.x<20:
            self.dirx=1

        if self.y>980:
            self.diry=-1
        elif self.y<20:
            self.diry=1
            self.rotation=self.rotation+1

        self.x=self.x+self.dirx*self.speedx
        self.y = self.y + self.diry * self.speedy

        self.frame = (self.frame + 1) % 3

    def get_bb(self):
        return self.x-15,self.y-25,self.x+15,self.y+25
    def get_aa(self):
        return self.x, self.y

    def draw_bb(self):
        draw_rectangle(*self.get_bb())