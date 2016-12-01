
from pico2d import *
import game_framework
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


def draw(frame_time):
    global world

    world.draw(frame_time)



def handle_events(frame_time):
    global world

    world.handle_events(frame_time)
