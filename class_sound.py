import game_framework
import math
import random
from pico2d import*

class Sound:                        #적3 겐지
    def __init__(self):
        self.bgm = load_music('wave.mp3')
        self.bgm.set_volume(49)
        self.bgm.repeat_play()

        self.hero_atacksound = load_wav('hit_normal.wav')
        self.hero_atacksound.set_volume(30)

        self.genji_dead = load_wav('genji_dead.wav')
        self.genji_dead.set_volume(51)

        self.bastion_dead = load_wav('bastion_dead.wav')
        self.bastion_dead.set_volume(51)

        self.reinhartd_dead = load_wav('reinhartd_dead.wav')
        self.reinhartd_dead.set_volume(51)

        self.item_get = load_wav('item_charge.wav')
        self.item_get.set_volume(40)

        self.boss_dada = load_wav('boss_dada.wav')
        self.boss_dada.set_volume(30)