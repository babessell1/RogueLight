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
        self.set_mouse_visible(True)
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
        self.cast = False
        self.mouse_x = 0
        self.mouse_y = 0

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
        self.Game.fps = int(pyg.clock.get_fps())
        self.clear()
        self.Game.draw_map()
        self.Game.draw_gui()
        self.Game.draw_debug()
        self.Game.draw_message()

        if self.cast:
            self.Game.draw_highlight(self.mouse_x, self.mouse_y, constants.COLOR_HILIGHT)

    def on_mouse_press(self, x, y, button, modifiers):
        if button==4:
            print("player", self.Game.game_objects["PLAYER"].x, self.Game.game_objects["PLAYER"].y)
            pass
        if button==1:
            if self.cast:
                self.cast = False
                choice = "FIREBALL"
                self.clear()
                self.Game.game_objects["PLAYER"].creature.cast_spell(self.Game,
                                            self.mouse_x, self.mouse_y, choice)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.cast:
            self.mouse_x = x
            self.mouse_y = y
            self.Game.draw_highlight(x, y, constants.COLOR_HILIGHT)

    def on_key_press(self, symbol, modifiers):
        self.cast = False
        moveFlag = False
        if symbol == pyg.window.key.UP: # player move up
            self.Game.game_objects["PLAYER"].direction = "up"
            self.Game.game_objects["PLAYER"].creature.move(self.Game, 0,  1)
            #self.Game.game_objects["PLAYER"].sprite = constants.UP_SPRITES["PLAYER"]
            moveFlag = True
        elif symbol == pyg.window.key.DOWN:
            self.Game.game_objects["PLAYER"].direction = "down"
            self.Game.game_objects["PLAYER"].creature.move(self.Game, 0, -1)
            #self.Game.game_objects["PLAYER"].sprite = constants.DOWN_SPRITES["PLAYER"]
            moveFlag = True
        elif symbol == pyg.window.key.LEFT:
            self.Game.game_objects["PLAYER"].direction = "left"
            self.Game.game_objects["PLAYER"].creature.move(self.Game, -1, 0)
            #self.Game.game_objects["PLAYER"].sprite = constants.LEFT_SPRITES["PLAYER"]
            moveFlag = True
        elif symbol == pyg.window.key.RIGHT:
            self.Game.game_objects["PLAYER"].direction = "right"
            self.Game.game_objects["PLAYER"].creature.move(self.Game,  1, 0)
            #self.Game.game_objects["PLAYER"].sprite = constants.RIGHT_SPRITES["PLAYER"]
            moveFlag = True
        elif symbol == pyg.window.key.C:
            self.cast = True
            moveFlag=True
        elif symbol == pyg.window.key.T:
            if self.Game.game_objects["PLAYER"].creature.mana>0 and self.Game.light_source=="torch":
                self.Game.light_source = "magic"
                self.Game.game_objects["PLAYER"].sprite = constants.S_PLAYER_MAGIC
            elif self.Game.game_objects["PLAYER"].creature.mana<1 and self.Game.light_source=="torch":
                self.Game.game_messages.append(("You are out of mana.", constants.COLOR_WHITE))
            elif self.Game.torch_counter>0 and self.Game.light_source=="magic":
                self.Game.light_source = "torch"
                self.Game.game_objects["PLAYER"].sprite = constants.S_PLAYER_TORCH
            elif self.Game.torch_counter<1 and self.Game.light_source=="magic":
                self.Game.game_messages.append(("Your torch is extinguished.", constants.COLOR_WHITE))
            elif self.Game.torch_counter<1 and self.Game.game_objects["PLAYER"].creature.mana<1:
                self.Game.game_messages.append(("Find a torch or more mana.", constants.COLOR_WHITE))
            moveFlag = True
            #hello


        if moveFlag:
            self.Game.turn += 1
            rmobj = []
            for obj in self.Game.game_objects.values():
                if obj.ai:
                    remove = obj.ai.play_turn(self.Game)
                    if remove:
                        rmobj.append(obj.obj_name)
            for obj in rmobj:
                self.Game.game_objects.pop(obj)

            self.Game.update = True

    def update(self, dt):
        pass


if __name__ == '__main__':
    window = GameWindow(1280, 720, "RogueLight", resizable=True)
    pyg.app.run()
    print("noodle")
    #game_initialize()
    #game_main_loop()
