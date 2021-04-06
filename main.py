import pygame
import pyglet as pyg
import tcod
import constants
import random
import numpy as np
import time
import math
from game import *


class GameWindow(pyg.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fix sizes to be compatible with cell sizes
        self.set_minimum_size(576, 576)
        w = self.width
        h = self.height
        w = (w//(2*constants.CELL_WIDTH) )*constants.CELL_WIDTH*2
        h = (h//(2*constants.CELL_HEIGHT))*constants.CELL_HEIGHT*2
        self.width = w
        self.height = h
        self.Game = Game(w, h, constants.CELL_WIDTH,
                       constants.MAP_WIDTH, constants.MAP_HEIGHT,
                       level=1, light_source="torch")
        self.tick = 0

        '''def callback(dt):
            self.tick +=1
            for obj in self.Game.game_objects.values():
                obname = list(constants.MONSTER_NAMES.keys())[
                    list(constants.MONSTER_NAMES.values()).index(obj.obj_name)]
                if obj.direction == "right":
                    obj.sprite = constants.RIGHT_SPRITES[obname]

                elif obj.direction == "left":
                    obj.sprite = constants.LEFT_SPRITES[obname]

                elif obj.direction == "down":
                    obj.sprite = constants.DOWN_SPRITES[obname]

                if obj.direction == "up":
                    obj.sprite = constants.UP_SPRITES[obname]

            self.Game.update = True

        pyg.clock.schedule_interval(callback, 0.5)'''

    def title_draw(self):
        self.clear()
        lab_text = "RogueLight"
        label = pyg.text.Label(lab_text,
                              font_name="Dungeon",
                              font_size=66,
                              x=self.width//2, y=self.height//2,
                              anchor_x='center', anchor_y='center')
        label.draw()

    def on_draw(self):
        self.width = (self.width//(constants.CELL_WIDTH*2))*constants.CELL_WIDTH*2
        self.height = (self.height//(constants.CELL_HEIGHT*2))*constants.CELL_HEIGHT*2
        self.Game.window_width = self.width
        self.Game.window_height = self.height
        self.clear()
        self.Game.draw_map()
        self.Game.draw_gui()
        self.Game.draw_debug()
        self.Game.draw_message()

    def on_key_press(self, symbol, modifiers):
        moveFlag = False
        if symbol == pyg.window.key.UP: # player move up
            self.Game.game_objects["PLAYER"].direction = "up"
            self.Game.game_objects["PLAYER"].creature.move(self.Game, 0,  1)
            self.Game.game_objects["PLAYER"].sprite = constants.UP_SPRITES["PLAYER"]
            moveFlag = True
        elif symbol == pyg.window.key.DOWN:
            self.Game.game_objects["PLAYER"].direction = "down"
            self.Game.game_objects["PLAYER"].creature.move(self.Game, 0, -1)
            self.Game.game_objects["PLAYER"].sprite = constants.DOWN_SPRITES["PLAYER"]
            moveFlag = True
        elif symbol == pyg.window.key.LEFT:
            self.Game.game_objects["PLAYER"].direction = "left"
            self.Game.game_objects["PLAYER"].creature.move(self.Game, -1, 0)
            self.Game.game_objects["PLAYER"].sprite = constants.LEFT_SPRITES["PLAYER"]
            moveFlag = True
        elif symbol == pyg.window.key.RIGHT:
            self.Game.game_objects["PLAYER"].direction = "right"
            self.Game.game_objects["PLAYER"].creature.move(self.Game,  1, 0)
            self.Game.game_objects["PLAYER"].sprite = constants.RIGHT_SPRITES["PLAYER"]
            moveFlag = True
        if moveFlag:
            self.Game.turn += 1
            for obj in self.Game.game_objects.values():
                if obj.ai:
                    obj.ai.play_turn(self.Game)
            self.Game.update = True


if __name__ == '__main__':
    window = GameWindow(1280, 720, "RogueLight", resizable=True)
    pyg.app.run()
    print("noodle")
    #game_initialize()
    #game_main_loop()
