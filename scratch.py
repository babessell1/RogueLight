import random
import numpy as np


class obj_Actor:
    def __init__(self, x, y, obj_name, sprite, creature=None, ai=None, light=0, color=None, death_function=None):
        self.x = x # map address
        self.y = y # map address
        self.obj_name = obj_name
        self.sprite = sprite
        self.light = light
        self.death_function = death_function

        self.creature = creature
        if creature:
            self.creature = creature
            creature.owner = self
        self.ai = ai
        if ai:
            self.ai = ai
            ai.owner = self


monster = obj_Actor(10, 10, "chicken", "turkey")

OBJ = {}

OBJ["MONSTER"] = monster

print(OBJ["MONSTER"])
