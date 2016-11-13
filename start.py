from pico2d import *

class Map:
    image=None
    def __init__(self, xx,yy):
        self.x=xx
        self.y=yy
        if Map.image==None:
            Map.image = load_image('map.png')
    def draw(self):
        self.image.draw(self.x,self.y)
    def update(self):
        if self.y >-290:
            self.y=self.y-10
        else:
            self.y=900
#g
class bullet:
    image=None
    def __init__(self, xx,yy,spe):
        self.x=xx
        self.y=yy
        self.speed=spe
        if bullet.image==None:
            bullet.image = load_image('soundwave.png')
    def draw(self):
        if self.y < 800:
            self.image.draw(self.x,self.y)
    def update(self):
        if self.y<800:
            self.y=self.y+self.speed
    def get_bb(self):
        return self.x-15,self.y-15,self.x+15,self.y+15


class Enemy:
    image=None
    def __init__(self, xx,yy):
        self.x=xx
        self.y=yy
        self.frame=0
        self.hp=2
        if Enemy.image==None:
            Enemy.image = load_image('enemy.png')
    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
    def update(self):
        self.frame=(self.frame+1)%2
    def get_bb(self):
        return self.x-50,self.y-50,self.x+50,self.y+50
    def get_xy(self):
        return

class Enemybullet:
    image=None
    def __init__(self, xx,yy,spe):
        self.x=xx
        self.y=yy
        self.speed=spe
        if Enemybullet.image==None:
            Enemybullet.image = load_image('enemybullet.png')
    def draw(self):
        if self.y < 800:
            self.image.draw(self.x,self.y)
    def update(self):
        if self.y>-100:
            self.y=self.y-self.speed
    def get_bb(self):
        return self.x-8,self.y-15,self.x+8,self.y+15


running =True

open_canvas()

character=load_image('charactersample.png')




x_right=False
x_left=False
y_up=False
y_down=False




x=400
y=90
frame=0

tan=[bullet(x,700,10)]
tani=1

map=[Map(400,300),Map(400,900)]

enemy=[Enemy(300,500),Enemy(600,500)]
enemyi=2

enemytan=[Enemybullet(300,500,10),Enemybullet(300,500,10)]
enemytani=2

tanframe=0

hp=2


def handle_events():
    global running
    global x_right
    global x_left
    global y_up
    global y_down
    global tani
    global x, y


    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            running =False
        elif event.type==SDL_KEYDOWN:
            if event.key==SDLK_RIGHT:
                x_right=True
            elif event.key==SDLK_LEFT:
                x_left = True
            elif event.key==SDLK_UP:
                y_up=True
            elif event.key==SDLK_DOWN:
                y_down=True
            elif event.key==SDLK_ESCAPE:
                running=False
            if event.key == SDLK_SPACE:
                if tani<50:
                    tani = tani + 1
                    tan.insert(tani%50,bullet(x,y,15))
                else:
                    tani = tani + 1
                    tan[tani%50]=bullet(x, y, 15)


        elif event.type == SDL_KEYUP:
            if event.key==SDLK_RIGHT:
                x_right=False
            elif event.key==SDLK_LEFT:
                x_left = False
            elif event.key==SDLK_UP:
                y_up=False
            elif event.key==SDLK_DOWN:
                y_down=False

def update():
    global frame
    global x_right
    global x_left
    global y_up
    global y_down
    global x, y
    global enemyi
    global enemytani
    global eenn
    global tanframe
    global hp

    frame = (frame + 1) % 3

    delay(0.05)
    handle_events()

    map[0].update()
    map[1].update()

    #탄의 개수
    if tani<50:
        for i in range(0, tani):
            tan[i].update()
    else:
        for i in range(0, 50):
            tan[i].update()

    for i in range(0, enemyi):
        enemy[i].update()
        if tani < 50:
            for j in range(0, tani):
                if collide(enemy[i],tan[j]):
                    enemy[i].y=800
                    enemy[i].x = 900
        else:
            for j in range(0, 50):
                tan[j].update()



    if enemytani<50:
        for i in range(0, enemytani):
            enemytan[i].update()
    else:
        for i in range(0, 50):
            enemytan[i].update()

    if tanframe>0:
        tanframe=(tanframe+1)%5

    for i in range(0,enemyi):
        if  tancllide(enemy[i],x,y)==True and tanframe==0:
            tanframe=1
            enemytan.insert(enemytani,Enemybullet(enemy[i].x,enemy[i].y,15))
            enemytani=enemytani+1

    if enemytani<50:
        for i in range(0,enemytani):
            if bodyat(x,y,enemytan[i])==True:
                hp=hp-1
                if hp==0:
                    x,y=0,0
    else:
        for i in range(0,50):
            if bodyat(x,y,enemytan[i])==True:
                hp=hp-1
                if hp==0:
                    x,y=0,0


    if x_right == True and x<=660:
        x = x + 10
    if x_left == True and x>=140:
        x = x - 10
    if y_up == True and y<560:
        y = y + 10
    elif y_down == True and y>40:
        y = y - 10

def draw():
    global hp
    clear_canvas()

    map[0].draw()
    map[1].draw()

    if hp>0:
        character.clip_draw(frame * 80, 0, 80, 80, x, y)
    if tani<50:
        for i in range(0,tani):
            tan[i].draw()
    else:
        for i in range(0,50):
            tan[i].draw()

    if enemytani<50:
        for i in range(0,enemytani):
            enemytan[i].draw()
    else:
        for i in range(0,50):
            enemytan[i].draw()


    for i in range(0, enemyi):
        enemy[i].draw()
    update_canvas()

def collide(a,b):  #a:anemy b:tan
    left_a,bottom_a,right_a,top_a=a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a>right_b: return False
    if right_a<left_b: return False


    if top_a< bottom_b: return False
    if bottom_a> top_b: return False

    return True

def tancllide(a,x,y): #a:anemy b:tan
    left_a, bottom_a, right_a, top_a = a.get_bb()
    if left_a>x+5: return False
    if right_a<x-5: return False

    return True

def bodyat(x,y,a):  #a:anemy b:tan
    left_a,bottom_a,right_a,top_a=a.get_bb()

    if left_a>x+40: return False
    if right_a<x-40: return False
    if top_a< y-40: return False
    if bottom_a> y+40: return False

    return True

while(running):
    update()
    draw()

close_canvas()