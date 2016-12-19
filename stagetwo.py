
from pico2d import *
import game_framework
import gameover
from worldtwo import worldclass




world=None


def enter():
    global world
    world=worldclass()

def exit():
    global world
    del(world)

def update(frame_time):
    global world

    world.update(frame_time)
    if world.restart==1:
        world.restart=0
        game_framework.change_state(gameover)

def draw(frame_time):
    global world

    world.draw(frame_time)



def handle_events(frame_time):
    global world

    world.handle_events(frame_time)
