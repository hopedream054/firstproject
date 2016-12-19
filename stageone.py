
from pico2d import *
import game_framework
import stagetwo
import gameover
from world import worldclass




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
    if world.stage==1:
        game_framework.change_state(stagetwo)
    elif world.restart==1:
        world.restart=0
        game_framework.change_state(gameover)


def draw(frame_time):
    global world

    world.draw(frame_time)



def handle_events(frame_time):
    global world

    world.handle_events(frame_time)
