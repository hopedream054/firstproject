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
    global image,bgm,gamestart
    image = load_image('gameover.png')
    bgm = load_music('gameover.mp3')
    bgm.set_volume(49)
    bgm.repeat_play()
    gamestart=0
def exit():
    global image
    del(image)

def update(frame_time):
    global name,gamestart
    global logo_time, gamestart,menuframe

    if (logo_time > 0.15):
        logo_time = 0

        if gamestart==1:
            game_framework.push_state(stageone)
        #game_framework.quit()
    logo_time += frame_time

def draw(frame_time):
    global image,menuframe
    clear_canvas()
    image.draw(400, 500)
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




