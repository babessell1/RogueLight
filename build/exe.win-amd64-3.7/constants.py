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
MAP_WIDTH = 50
MAP_HEIGHT = 30

# FONT SETTINGS
FONT_DEBUG_MESSAGE = pygame.font.Font("data/DUNGRG.TTF", 40)
FONT_MESSAGE_TEXT = pygame.font.Font("data/DUNGRG.TTF", 20)

# Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = [255, 15, 15]

# Game Colors
COLOR_DEFAULT_BG = COLOR_BLACK

# Sprites
S_PLAYER = pygame.image.load("data/player_test.png")

S_WALL = pygame.image.load("data/wall1.png")
S_FLOOR = pygame.image.load("data/floor1.png")
S_WALL_EX = pygame.image.load("data/wall1.png")
S_FLOOR_EX = pygame.image.load("data/floor1.png")

S_WALL_EX.fill ((40,50,60), special_flags=pygame.BLEND_RGBA_MULT)
S_FLOOR_EX.fill ((40,50,60), special_flags=pygame.BLEND_RGBA_MULT)


S_SKELETON_REG_BROKEN = pygame.image.load("data/skele_broken.png")
S_MUMMY = pygame.image.load("data/mummy.png")
S_ZOMBIE = pygame.image.load("data/zombie.png")

#FOV SETTINGS
FOV_ALG = tcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

# Message Defaults
NUM_MESSAGES = 4
