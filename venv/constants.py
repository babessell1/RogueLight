import pygame
import pyglet as pyg
import tcod
import math

pygame.init()

# FPS Limit
GAME_FPS = 60

# Resolution
SCREEN_X = 1920
SCREEN_Y = 1200

# Game Sizes
CELL_WIDTH = 32
CELL_HEIGHT = 32

# Map vars
MAP_WIDTH = int(100)
MAP_HEIGHT = int(100)

MAP_BUFFER = 25
GUI_WIDTH = 32*10
#MAP_HEIGHT = int(30*2)



#FOV SETTINGS
FOV_ALG = tcod.FOV_BASIC
FOV_LIGHT_WALLS = True

# FONT SETTINGS
#FONT_DEBUG_MESSAGE = pygame.font.Font("data/DUNGRG.TTF", 40)
#FONT_MESSAGE_TEXT = pygame.font.Font("data/DUNGRG.TTF", 20)
pyg.resource.add_font("data/DUNGRG.TTF")
FONT_DEBUG_MESSAGE = pyg.font.load("Dungeon Font", 40)

pyg.resource.add_font("data/DUNGRG.TTF")
FONT_MESSAGE_TEXT = pyg.font.load("Dungeon Font", 20)

pyg.resource.add_font("data/DUNGRG.TTF")
FONT_TITLE = pyg.font.load("Dungeon")

# TORCH SETTINGS
INIT_MANA = 200
INIT_HP = 10
INIT_ATK = 2
INIT_TORCH_CHARGE = 2000
MAGIC_LIGHT_RADIUS = 10
E_LIGHT_RADIUS = 2
BASE_TORCH_RADIUS = 9
MANA_COUNT_THRESH = 10
TORCH_COUNT_THRESH = 50

# Color definitions
COLOR_BLACK = (0, 10, 20)
COLOR_WALL = (50, 50, 50)
COLOR_BROWN = (100, 80, 100)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_GREY = (60, 60, 60)
COLOR_RED = (255, 50, 50, 255)
COLOR_BLUE = (60, 120, 200, 255)
COLOR_YELLOW = (240, 240, 50, 255)
COLOR_TORCHLIGHT = (240, 120, 50)
COLOR_MAGICLIGHT = (50, 150, 250)
COLOR_HILIGHT = (255, 255, 0)
COLOR_CLIP = 40

COLOR_TORCH_MAG_BLEND = (int((COLOR_TORCHLIGHT[0]+COLOR_MAGICLIGHT[0])/2),
                         int((COLOR_TORCHLIGHT[1]+COLOR_MAGICLIGHT[1])/2),
                         int((COLOR_TORCHLIGHT[2]+COLOR_MAGICLIGHT[2])/2))

# Game Colors
COLOR_DEFAULT_BG = COLOR_BLACK

# Sprites
#S_PLAYER = pyg.image.load("data/creatures/player_test.png")
S_PLAYER_LEFT = pyg.resource.image('data/creatures/player_torch_left.png')
S_PLAYER_RIGHT = pyg.resource.image('data/creatures/player_torch_right.png')
S_PLAYER_DOWN = pyg.resource.image('data/creatures/player_torch_down.png')
S_PLAYER_UP = pyg.resource.image('data/creatures/player_torch_up.png')

a_player = [S_PLAYER_LEFT, S_PLAYER_DOWN, S_PLAYER_RIGHT, S_PLAYER_DOWN]
A_PLAYER = pyg.image.Animation.from_image_sequence(a_player, duration = 1.0, loop=True)

LEFT_SPRITES = {"PLAYER" : pyg.image.load("data/creatures/player_torch_left.png"),
                "SKELETON" : pyg.image.load("data/creatures/skeleton_1.png"),
                "MUMMY" : pyg.image.load("data/creatures/mummy_1.png"),
                "ZOMBIE" : pyg.image.load("data/creatures/zombie_1.png"),
                "SKULL" : pyg.image.load("data/creatures/glow_skull.png") }

DOWN_SPRITES = {"PLAYER" : pyg.image.load("data/creatures/player_torch_down.png"),
                "SKELETON" : pyg.image.load("data/creatures/skeleton_1.png"),
                "MUMMY" : pyg.image.load("data/creatures/mummy_1.png"),
                "ZOMBIE" : pyg.image.load("data/creatures/zombie_1.png"),
                "SKULL" : pyg.image.load("data/creatures/glow_skull.png") }

RIGHT_SPRITES = {"PLAYER" : pyg.image.load("data/creatures/player_torch_right.png"),
                "SKELETON" : pyg.image.load("data/creatures/skeleton_1.png"),
                "MUMMY" : pyg.image.load("data/creatures/mummy_1.png"),
                "ZOMBIE" : pyg.image.load("data/creatures/zombie_1.png"),
                "SKULL" : pyg.image.load("data/creatures/glow_skull.png") }

UP_SPRITES = {"PLAYER" : pyg.image.load("data/creatures/player_torch_up.png"),
                "SKELETON" : pyg.image.load("data/creatures/skeleton_1.png"),
                "MUMMY" : pyg.image.load("data/creatures/mummy_1.png"),
                "ZOMBIE" : pyg.image.load("data/creatures/zombie_1.png"),
                "SKULL" : pyg.image.load("data/creatures/glow_skull.png") }



# monsters
MONSTER_SPRITES = {
                "SKELETON_1" : pyg.image.load("data/creatures/skeleton_1.png"),
                "SKELETON_2" : pyg.image.load("data/creatures/skeleton_2.png"),
                "SKELETON_3" : pyg.image.load("data/creatures/skeleton_3.png"),
                "MUMMY_1" : pyg.image.load("data/creatures/mummy_1.png"),
                "MUMMY_2" : pyg.image.load("data/creatures/mummy_2.png"),
                "MUMMY_3" : pyg.image.load("data/creatures/mummy_3.png"),
                "ZOMBIE_1" : pyg.image.load("data/creatures/zombie_1.png"),
                "ZOMBIE_2" : pyg.image.load("data/creatures/zombie_2.png"),
                "ZOMBIE_3" : pyg.image.load("data/creatures/zombie_3.png"),
                "SKULL_1" : pyg.image.load("data/creatures/glow_skull.png") }

MONSTER_DEATH_SPRITES = {
                 "PLAYER" : pyg.image.load("data/creatures/player_torch_up.png"),
                 "SKELETON" : pyg.image.load("data/creatures/skeleton_1.png"),
                 "MUMMY" : pyg.image.load("data/creatures/mummy_1.png"),
                 "ZOMBIE" : pyg.image.load("data/creatures/zombie_1.png"),
                 "SKULL" : pyg.image.load("data/creatures/glow_skull.png") }

MONSTER_NAMES = { # display name
                "PLAYER" : "player",
              "SKELETON" : "skeleton",
                 "MUMMY" : "mummy",
                "ZOMBIE" : "zombie",
                 "SKULL" : "glowing skull" }

MONSTER_HP = { # max health
              "SKELETON" : 5,
                 "MUMMY" : 3,
                "ZOMBIE" : 3,
                 "SKULL" : 1 }

MONSTER_INI = { # initiative
               "SKELETON" : 1,
                  "MUMMY" : 2,
                 "ZOMBIE" : 3,
                  "SKULL" : 1 }

MONSTER_SPD = { # speed (tiles to jump)
               "SKELETON" : 1,
                  "MUMMY" : 2,
                 "ZOMBIE" : 1,
                  "SKULL" : 2 }

MONSTER_ATK = { # attack damage
               "SKELETON" : 1,
                  "MUMMY" : 2,
                 "ZOMBIE" : 3,
                  "SKULL" : 5 }

MONSTER_SPELLS = {
                  "SKELETON" : ["melee", "ranged"],
                     "MUMMY" : ["melee"],
                    "ZOMBIE" : ["melee"],
                     "SKULL" : ["melee"] }

MONSTER_SPELL_WEIGHTS = {
                        "SKELETON" : [1, 2],
                           "MUMMY" : [1],
                          "ZOMBIE" : [1],
                           "SKULL" : [1] }

MONSTER_LGT = { # light emission
               "SKELETON" : 0,
                  "MUMMY" : 0,
                 "ZOMBIE" : 0,
                  "SKULL" : 4 }

MONSTER_COL = { # light color
               "SKELETON" : None,
                  "MUMMY" : None,
                 "ZOMBIE" : None,
                  "SKULL" : COLOR_MAGICLIGHT }

# Spells
SPELL_NAMES = {
            "FIREBALL" : "fireball" }

SPELL_SPRITES = {
            "FIREBALL" : pyg.image.load("data/spells/fire.png") }

SPELL_KEYS = {
            "FIREBALL" : "F" }

SPELL_BINDINGS = {
            "FIREBALL" : pygame.K_f }

SPELL_COLORS = {
            "FIREBALL" : (120, 80, 10) }

SPELL_LIGHT = {
            "FIREBALL" : 7 }

SPELL_EFFECTS = {
            "FIREBALL" : "fire" }

SPELL_PIERCE = {
            "FIREBALL" : False }

SPELL_RANGES = {
            "FIREBALL" : 5 }

SPELL_TYPES = {
            "FIREBALL" : "blast" }

SPELL_SIZES = {
             "FIREBALL" : 3 }

SPELL_IMPACT_DMG = {
             "FIREBALL" : 5 }

SPELL_AOE_DECAY = {
             "FIREBALL" : 1 }

SPELL_DURATIONS = {
             "FIREBALL" : 3 }

## LOOT TABLES
LOOT_TAB_1 = {
            "FIREBALL" : 1 }

LOOT_TAB_MAP = [
            LOOT_TAB_1
]




#for key in MONSTER_DEATH_SPRITES:
    #MONSTER_DEATH_SPRITES[key].fill ((140,40,40), special_flags=pygame.BLEND_RGBA_MULT)





    # walls

'''
S_WALL = pyg.image.load("data/structures/wall1.png")
S_WALL.fill(COLOR_WALL,special_flags=pygame.BLEND_RGBA_MULT)

S_WALL_EX = pyg.image.load("data/structures/wall1.png")
S_WALL_EX.fill ((40,40,40), special_flags=pygame.BLEND_RGBA_MULT)
'''
S_FILT = pyg.image.load("data/structures/filter.png")
S_WALL = pyg.image.load("data/structures/wall1.png")
S_WALL.color=COLOR_WALL
S_WALL_TLIGHT = pyg.image.load("data/structures/wall1.png")
S_WALL_TLIGHT.color=COLOR_TORCHLIGHT
S_WALL_EX = pyg.image.load("data/structures/wall1.png")
S_WALL_EX.color=(40,40,40)

    # floor
'''
S_FLOOR = pyg.image.load("data/structures/floor1.png")
S_FLOOR.fill(COLOR_WALL,special_flags=pygame.BLEND_RGBA_MULT )
S_FLOOR_TLIGHT = pyg.image.load("data/structures/floor1.png")
S_FLOOR_TLIGHT.fill(COLOR_TORCHLIGHT, special_flags=pygame.BLEND_RGBA_MULT)
S_FLOOR_EX = pyg.image.load("data/structures/floor1.png")
S_FLOOR_EX.fill ((40,40,40), special_flags=pygame.BLEND_RGBA_MULT)
'''

S_FLOOR = pyg.image.load("data/structures/floor1.png")
S_FLOOR.color = COLOR_WALL
S_FLOOR_TLIGHT = pyg.image.load("data/structures/floor1.png")
S_FLOOR_TLIGHT.color = COLOR_TORCHLIGHT
S_FLOOR_EX = pyg.image.load("data/structures/floor1.png")
S_FLOOR_EX.color = (10,10,10)

# Message Defaults
NUM_MESSAGES = 4
