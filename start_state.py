import game_framework
import stageone
import stagetwo

from pico2d import *



name = "StartState"
bgm=None
image = None
clickimage = None
logo_time = 0.0
gamestart=0
menuframe=0

def enter():
    global image,clickimage,bgm
    image = load_image('startbackground.png')
    clickimage=load_image('startclick.png')
    bgm = load_music('startbgm.mp3')
    bgm.set_volume(49)
    bgm.repeat_play()

def exit():
    global image
    del(image)

def update(frame_time):
    global name
    global logo_time, gamestart,menuframe

    if (logo_time > 0.15):
        logo_time = 0
        menuframe=(menuframe+1)%10

        if gamestart==1:
            game_framework.push_state(stagetwo)
        #game_framework.quit()
    logo_time += frame_time

def draw(frame_time):
    global image,clickimage,menuframe
    clear_canvas()
    image.draw(400, 500)
    clickimage.clip_draw(0, menuframe * 100, 800, 100, 400, 100)

    update_canvas()

def handle_events(frame_time):
    global gamestart
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                gamestart = 1

def pause(): pass
def resume(): pass




