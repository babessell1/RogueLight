import pygame
import tcod

pygame.init()

# FPS Limit
GAME_FPS = 60

# Game Sizes
GAME_WIDTH = 960
GAME_HEIGHT = 960
CELL_WIDTH = 32
CELL_HEIGHT = 32

# Map vars
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 30
MAP_WIDTH = int(50*2)
MAP_HEIGHT = int(50*2)

MAP_BUFFER = 25
#MAP_HEIGHT = int(30*2)



#FOV SETTINGS
FOV_ALG = tcod.FOV_BASIC
FOV_LIGHT_WALLS = True

# FONT SETTINGS
FONT_DEBUG_MESSAGE = pygame.font.Font("data/DUNGRG.TTF", 40)
FONT_MESSAGE_TEXT = pygame.font.Font("data/DUNGRG.TTF", 20)

# TORCH SETTINGS
INIT_MANA = 20
MAGIC_LIGHT_RADIUS = 10
E_LIGHT_RADIUS = 2
MAX_TORCH_RADIUS = 7
MANA_COUNT_THRESH = 10
TORCH_COUNT_THRESH = 50

# Color definitions
COLOR_BLACK = (0, 10, 20)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = (255, 15, 15)
COLOR_BLUE = (60, 160, 240)
COLOR_YELLOW = (240, 240, 20)
COLOR_TORCHLIGHT = (100, 50, 1)
COLOR_MAGICLIGHT = (1, 25, 100)
COLOR_HILIGHT = (255, 255, 0)

COLOR_TORCH_MAG_BLEND = (int((COLOR_TORCHLIGHT[0]+COLOR_MAGICLIGHT[0])/2),
                         int((COLOR_TORCHLIGHT[1]+COLOR_MAGICLIGHT[1])/2),
                         int((COLOR_TORCHLIGHT[2]+COLOR_MAGICLIGHT[2])/2))

# Game Colors
COLOR_DEFAULT_BG = COLOR_BLACK

# Sprites
S_PLAYER = pygame.image.load("data/creatures/player_test.png")

# monsters
MONSTER_SPRITES = {
                "SKELETON_1" : pygame.image.load("data/creatures/skeleton_1.png"),
                "SKELETON_2" : pygame.image.load("data/creatures/skeleton_2.png"),
                "SKELETON_3" : pygame.image.load("data/creatures/skeleton_3.png"),
                "MUMMY_1" : pygame.image.load("data/creatures/mummy_1.png"),
                "MUMMY_2" : pygame.image.load("data/creatures/mummy_2.png"),
                "MUMMY_3" : pygame.image.load("data/creatures/mummy_3.png"),
                "ZOMBIE_1" : pygame.image.load("data/creatures/zombie_1.png"),
                "ZOMBIE_2" : pygame.image.load("data/creatures/zombie_2.png"),
                "ZOMBIE_3" : pygame.image.load("data/creatures/zombie_3.png"),
                "SKULL_1" : pygame.image.load("data/creatures/glow_skull.png") }

MONSTER_DEATH_SPRITES = {
                "SKELETON_1" : pygame.image.load("data/creatures/skeleton_1.png"),
                "SKELETON_2" : pygame.image.load("data/creatures/skeleton_2.png"),
                "SKELETON_3" : pygame.image.load("data/creatures/skeleton_3.png"),
                "MUMMY_1" : pygame.image.load("data/creatures/mummy_1.png"),
                "MUMMY_2" : pygame.image.load("data/creatures/mummy_2.png"),
                "MUMMY_3" : pygame.image.load("data/creatures/mummy_3.png"),
                "ZOMBIE_1" : pygame.image.load("data/creatures/zombie_1.png"),
                "ZOMBIE_2" : pygame.image.load("data/creatures/zombie_2.png"),
                "ZOMBIE_3" : pygame.image.load("data/creatures/zombie_3.png"),
                "SKULL_1" : pygame.image.load("data/creatures/glow_skull.png") }

MONSTER_NAMES = { # display name
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
            "FIREBALL" : pygame.image.load("data/spells/fire.png") }

SPELL_KEYS = {
            "FIREBALL" : "F" }

SPELL_BINDINGS = {
            "FIREBALL" : pygame.K_f }

SPELL_COLORS = {
            "FIREBALL" : (120, 80, 10) }

SPELL_EFFECTS = {
            "FIREBALL" : "fire" }

SPELL_PIERCE = {
            "FIREBALL" : False }

SPELL_RANGES = {
            "FIREBALL" : 5 }

SPELL_SHAPES = {
            "FIREBALL" : "single_target" }

SPELL_SIZES = {
             "FIREBALL" : 1 }

SPELL_DURATIONS = {
            "FIREBALL" : 3 }



#for key in MONSTER_DEATH_SPRITES:
    #MONSTER_DEATH_SPRITES[key].fill ((140,40,40), special_flags=pygame.BLEND_RGBA_MULT)





    # walls
S_WALL = pygame.image.load("data/structures/wall1.png")
S_WALL_TLIGHT = pygame.image.load("data/structures/wall1.png")
S_WALL_TLIGHT.fill(COLOR_TORCHLIGHT, special_flags=pygame.BLEND_RGBA_MULT)
S_WALL_EX = pygame.image.load("data/structures/wall1.png")
S_WALL_EX.fill ((40,50,60), special_flags=pygame.BLEND_RGBA_MULT)

    # floor
S_FLOOR = pygame.image.load("data/structures/floor1.png")
S_FLOOR_TLIGHT = pygame.image.load("data/structures/floor1.png")
S_FLOOR_TLIGHT.fill(COLOR_TORCHLIGHT, special_flags=pygame.BLEND_RGBA_MULT)
S_FLOOR_EX = pygame.image.load("data/structures/floor1.png")
S_FLOOR_EX.fill ((40,50,60), special_flags=pygame.BLEND_RGBA_MULT)


# Message Defaults
NUM_MESSAGES = 4
