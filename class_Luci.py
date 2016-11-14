import random
import game_framework

from pico2d import*
x_right=x_left=y_up=y_down=None
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