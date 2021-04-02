
#   __                          __ _       _     _
#  /__\ ___   __ _ _   _  ___  / /(_) __ _| |__ | |_
# / \/// _ \ / _` | | | |/ _ \/ / | |/ _` | '_ \| __|
#/ _  \ (_) | (_| | |_| |  __/ /__| | (_| | | | | |_
#\/ \_/\___/ \__, |\__,_|\___\____/_|\__, |_| |_|\__|
#            |___/                   |___/

# By Brandt Bessell

import pygame
import tcod
import constants
import random
import numpy as np
import time
import math

# __ _                   _
#/ _\ |_ _ __ _   _  ___| |_ _   _ _ __ ___  ___
#\ \| __| '__| | | |/ __| __| | | | '__/ _ \/ __|
#_\ \ |_| |  | |_| | (__| |_| |_| | | |  __/\__ \
#\__/\__|_|   \__,_|\___|\__|\__,_|_|  \___||___/

class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False

class camera():
    def __init__(self, x, y):
        self.x


#   ___ _     _           _
#  /___\ |__ (_) ___  ___| |_ ___
# //  // '_ \| |/ _ \/ __| __/ __|
#/ \_//| |_) | |  __/ (__| |_\__ \
#\___/ |_.__// |\___|\___|\__|___/
#          |__/

class obj_Actor:
    def __init__(self, x, y, obj_name, sprite, creature=None, ai=None, light=0, color=None, death_function=None):
        self.x = x # map address
        self.y = y # map address
        self.obj_name = obj_name
        self.sprite = sprite
        self.light = light
        self.color = color
        self.death_function = death_function

        self.creature = creature
        if creature:
            self.creature = creature
            creature.owner = self
        self.ai = ai
        if ai:
            self.ai = ai
            ai.owner = self


    def draw(self):
        if self.obj_name=="player":
            #print(constants.SCREEN_WIDTH/2*constants.CELL_WIDTH)
            #print(constants.SCREEN_HEIGHT/2*constants.CELL_HEIGHT)
            SURFACE_MAIN.blit(self.sprite, (constants.SCREEN_WIDTH/2*constants.CELL_WIDTH, constants.SCREEN_HEIGHT/2*constants.CELL_HEIGHT) )
        else:
            if FOV_MAP[self.y,self.x]>0:
                rx = self.x - GAME_OBJECTS["PLAYER"].x
                ry = self.y - GAME_OBJECTS["PLAYER"].y
                SURFACE_MAIN.blit(self.sprite, ( (rx+constants.SCREEN_WIDTH/2)*constants.CELL_WIDTH, (ry+constants.SCREEN_HEIGHT/2)*constants.CELL_HEIGHT) )


class obj_Spell:
    def __init__(self, obj_name, spell_name, sprite, x, y, sx=None, sy=None, light=0,
                 color=None, effect=None, pierce=False, range=1, shape=None,
                 size=1, duration=0, ai=None):

        self.obj_name = obj_name
        self.spell_name = spell_name
        self.sprite = sprite
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.light = light
        self.color = color
        self.effect = effect
        self.pierce = pierce
        self.range = range
        self.shape = shape
        self.size = size
        self.duration = duration
        self.ai=None


    def draw(self):
        #print(self.x, GAME_OBJECTS["PLAYER"].x)
        #print(self.y, GAME_OBJECTS["PLAYER"].y)
        if FOV_MAP[self.y,self.x]>0:
            rx = self.x - GAME_OBJECTS["PLAYER"].x
            ry = self.y - GAME_OBJECTS["PLAYER"].y
            #print( (rx+constants.SCREEN_WIDTH/2)*constants.CELL_WIDTH )
            #print( (ry+constants.SCREEN_HEIGHT/2)*constants.CELL_HEIGHT )
            if self.shape=="single_target":
                #print(self.shape)
                SURFACE_MAIN.blit(self.sprite, ( (rx+constants.SCREEN_WIDTH/2)*constants.CELL_WIDTH, (ry+constants.SCREEN_HEIGHT/2)*constants.CELL_HEIGHT) )






#   ___                                             _
#  / __\___  _ __ ___  _ __   ___  _ __   ___ _ __ | |_ ___
# / /  / _ \| '_ ` _ \| '_ \ / _ \| '_ \ / _ \ '_ \| __/ __|
#/ /__| (_) | | | | | | |_) | (_) | | | |  __/ | | | |_\__ \
#\____/\___/|_| |_| |_| .__/ \___/|_| |_|\___|_| |_|\__|___/
#                     |_|

class comp_Creature:
    #hp,ini,spd,atk)
        def __init__(self, name_personal,  isplayer=False, hp=10, ini=1, spd=1,
                     atk=1):
                     #death_function = None):
            self.name_personal = name_personal
            self.isplayer = isplayer
            self.hp = hp
            self.maxhp = hp
            self.ini = ini
            self.spd = spd
            self.atk = atk
            #self.death_function = death_function

        def change_torch(self):
            global LIGHTSOURCE, TORCH_COLOR
            #global TORCH_COLOR, TORCH_RADIUS, MAGIC_LIGHT_RADIUS, LIGHTSOURCE
            #global MANA

            if LIGHTSOURCE=="torch" and MANA > 0:
                LIGHTSOURCE = "magic"
                TORCH_COLOR = constants.COLOR_MAGICLIGHT

            elif LIGHTSOURCE=="magic" and TORCH_RADIUS > 1:
                LIGHTSOURCE = "torch"
                TORCH_COLOR = constants.COLOR_TORCHLIGHT

            else:
                LIGHTSOURCE = "emergency"
                TORCH_COLOR = constants.COLOR_MAGICLIGHT


        def move(self, dx, dy):
            #tile_isWall = (GAME_MAP.walkable[self.owner.y + dy][self.owner.x + dx] == False)
            tile_isWall = (GAME_MAP.walkable[(self.owner.y + dy),(self.owner.x + dx)] == False)

            target = map_check_creature(self.owner.x + dx, self.owner.y + dy, self.owner)

            if target:
                self.attack(target, self.atk)

            #new_map = GAME_MAP
            if not tile_isWall and target is None:
                self.owner.x += dx
                self.owner.y += dy

        def attack(self, target, damage):
            if target.creature.hp < 1:
                game_message(target.creature.name_personal + "is already dead.", constants.COLOR_WHITE)

            else:
                game_message(self.name_personal + " attacks " + target.creature.name_personal + " for " + str(damage) + " damage!", constants.COLOR_WHITE)
                target.creature.take_damage(damage)

        def take_damage(self, damage):
            self.hp -= damage
            game_message(self.name_personal + " HP: " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED)
            if self.hp <= 0:
                #self.death_function=death_monster
                if self.owner.death_function is not None:
                    self.owner.death_function(self.owner)

        def cast_spell(self):
            pushed=False
            cancel=False
            choice="NONE"
            while choice=="NONE":
                event_list = pygame.event.get()
                for event in event_list:
                    if event.type == pygame.KEYDOWN:
                        if event.key in constants.SPELL_BINDINGS.values():
                            choice = list(constants.SPELL_BINDINGS.keys())[
                                list(constants.SPELL_BINDINGS.values()).index(event.key)]
                            #choice = constants.SPELL_BINDINGS[k]
                            pass
                        if event.key == pygame.K_ESCAPE:
                            print("cancel")
                            return "idle"
            idx = 1
            objname = choice + "_" + str(idx)
            pickObj = False
            while not pickObj:
                if objname in GAME_OBJECTS.keys():
                    objname = choice + "_" + str(idx)
                else:
                    pickObj=True
                idx+=1
            pickLoc = False
            w = constants.CELL_WIDTH
            h = constants.CELL_HEIGHT
            hilight_surf = SURFACE_MAIN
            while not pickLoc:
                draw_game()
                for event in pygame.event.get():
                    if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                        print("cancel")
                        return "idle"
                    else:
                        pass
                #hilight_surf = pygame.display.set_mode( (constants.SCREEN_WIDTH*constants.CELL_WIDTH, constants.SCREEN_HEIGHT*constants.CELL_HEIGHT) )
                hilight_surf = SURFACE_MAIN
                #draw_map(hilight_surf)
                mpos = pygame.mouse.get_pos()
                tx = math.trunc(mpos[0]/w)
                ty = math.trunc(mpos[1]/h)
                mx = tx*w
                my = ty*h
                hilite = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))
                hilite.fill(constants.COLOR_HILIGHT, special_flags=pygame.BLEND_RGB_ADD)
                hilite.set_alpha(100)
                hilight_surf.blit(hilite, (mx, my))
                pygame.display.flip()

                if pygame.mouse.get_pressed()[0]:
                    px = self.owner.x
                    py = self.owner.y
                    rx = -1
                    adj_w = int(constants.SCREEN_WIDTH/2)
                    adj_h = int(constants.SCREEN_HEIGHT/2)
                    for x in range(px-adj_w,px+adj_w):
                        rx+=1
                        ry=-1
                        for y in range(py-adj_h,py+adj_h):
                            ry+=1
                            #rx*w, ry*h
                            if rx*w==mx and ry*h==my:
                                tx = px+rx-adj_w
                                ty = py+ry-adj_h
                                new_spell = obj_Spell(objname,
                                          constants.SPELL_NAMES[choice],
                                          constants.SPELL_SPRITES[choice],
                                          tx, ty,
                                          sx=px, sy=py, light=1,
                                          color=constants.SPELL_COLORS[choice],
                                          effect=None, pierce=False,
                                          range=constants.SPELL_RANGES[choice],
                                          shape=constants.SPELL_SHAPES[choice],
                                          size=constants.SPELL_SIZES[choice],
                                          duration=constants.SPELL_DURATIONS[choice])
                                GAME_OBJECTS[objname] = new_spell
                                return "moved"



#   _     _____
#  /_\    \_   \
# //_\\    / /\/
#/  _  \/\/ /_
#\_/ \_/\____/

class test_AI:
    def play_turn(self):
        self.owner.creature.move(tcod.random_get_int(0, -1, 1), tcod.random_get_int(0, -1, 1))

class random_walker_AI:
    def play_turn(self):
        #global TURN
        ini = self.owner.creature.ini
        if TURN % ini == 0:
            dist = self.owner.creature.spd
            neg_y = tcod.random_get_int(0, 0, 1)
            neg_x = tcod.random_get_int(0, 0, 1)
            x = dist
            y = dist
            if neg_x:
                x = -x
            if neg_y:
                y = -y
            #for i in range(self.owner.creature.spd):
            self.owner.creature.move(x, y)


class dead_AI():
    def play_turn(self):
        return


def death_monster(monster):
    game_message( monster.creature.name_personal + " is dead!", constants.COLOR_RED)
    #monster.creature = None
    monster.ai = dead_AI()
    monster.light = 0
    monster.sprite.fill ((180,40,40), special_flags=pygame.BLEND_RGBA_MULT)

def death_player(player):
    game_message( GAME_OBJECTS["PLAYER"].creature.name_personal + " is dead!", constants.COLOR_RED)
    game_message( "You survived " + str(TURN) + " turns!", constants.COLOR_YELLOW)
    GAME_OBJECTS["PLAYER"].creature.spd = 0

    #game_message(GAME_OBJECTS["PLAYER"].name_personal = " has died!!!")

#class comp_Item:

#class comp_Container:

#  /\/\   __ _ _ __
# /    \ / _` | '_ \
#/ /\/\ \ (_| | |_) |
#\/    \/\__,_| .__/
#             |_|

def map_create():

    new_map = tcod.map.Map(width=constants.MAP_WIDTH, height=constants.MAP_HEIGHT)
    new_map.explored = np.full((new_map.height, new_map.width), False, dtype=bool)
    new_map.walkable[:,:] = True

    new_map.walkable[:,0:constants.MAP_BUFFER] = False
    new_map.walkable[:,(constants.MAP_WIDTH-constants.MAP_BUFFER):constants.MAP_WIDTH] = False
    new_map.walkable[0:constants.MAP_BUFFER,:] = False
    new_map.walkable[(constants.MAP_HEIGHT-constants.MAP_BUFFER):constants.MAP_HEIGHT,:] = False

    FOV_MAP = tcod.map.compute_fov(new_map.walkable, (GAME_OBJECTS["PLAYER"].y, GAME_OBJECTS["PLAYER"].x), radius=TORCH_RADIUS, algorithm=tcod.FOV_SHADOW)
    COL_MAP_R = np.array(FOV_MAP, dtype=int)
    COL_MAP_G = COL_MAP_R
    COL_MAP_B = COL_MAP_R

    return new_map

def map_light_intensity(fov_map, radius, obj_x, obj_y):
    for x in range(len(fov_map[0,:])):
        for y in range(len(fov_map[:,0])):
            d = math.sqrt( ( (obj_x-x)*(obj_x-x) + (obj_y-y)*(obj_y-y) ) )
            if d<=radius:
                fov_map[y,x] = fov_map[y,x] * ( (radius/11)**d )
                #fov_map = np.clip(fov_map, 0, 1)



    return fov_map


def map_update_fov(game_map, px, py):
    colmaps_R = []
    colmaps_G = []
    colmaps_B = []
    if LIGHTSOURCE=="torch":
        rad = TORCH_RADIUS
    elif LIGHTSOURCE=="magic":
        rad = constants.MAGIC_LIGHT_RADIUS
    elif LIGHTSOURCE=="emergency":
        rad = constants.E_LIGHT_RADIUS

    fov_map = tcod.map.compute_fov(game_map.walkable, (py, px),
                                   radius=rad, algorithm=tcod.FOV_SHADOW)

    int_map = tcod.map.compute_fov(game_map.walkable, (py, px),
                                   radius=rad, algorithm=tcod.FOV_SHADOW)

    fov_map = np.array(fov_map, dtype=np.float16)
    int_map = np.array(int_map, dtype=np.float16)
    #print(fov_map)

    int_map = \
    map_light_intensity(int_map, rad, px, py)

    col_R = (fov_map*TORCH_COLOR[0])
    col_G = (fov_map*TORCH_COLOR[1])
    col_B = (fov_map*TORCH_COLOR[2])


    col_R[col_R==0] = np.nan
    col_G[col_G==0] = np.nan
    col_B[col_B==0] = np.nan
    colmaps_R.append(col_R)
    colmaps_G.append(col_G)
    colmaps_B.append(col_B)

    for obj in GAME_OBJECTS.values():
        if obj.light>0:
            fmap = tcod.map.compute_fov(game_map.walkable, (obj.y, obj.x),
                             radius=obj.light, algorithm=tcod.FOV_SHADOW)

            fmap = np.array(fmap, dtype=np.float16)

            imap = tcod.map.compute_fov(game_map.walkable, (obj.y, obj.x),
                             radius=obj.light, algorithm=tcod.FOV_SHADOW)

            imap = np.array(imap, dtype=np.float16)

            int_map += map_light_intensity(imap, obj.light, obj.x, obj.y)

            fov_map += fmap
            #fov_map = np.clip(fov_map, 0, 1)
            col_R = (fmap*obj.color[0])
            col_G = (fmap*obj.color[1])
            col_B = (fmap*obj.color[2])

            min_col = constants.COLOR_CLIP

            #col_R, col_G, col_B = \
            #map_light_intensity(fmap, rad, ox, oy, col_R, col_G, col_B)

            col_R[col_R==0] = np.nan
            col_G[col_G==0] = np.nan
            col_B[col_B==0] = np.nan
            colmaps_R.append(col_R)
            colmaps_G.append(col_G)
            colmaps_B.append(col_B)
            #print(colmaps_R[0][px+1, py+1])

    col_map_R = np.nanmean(colmaps_R, axis=0)
    #print(col_map_R[py+1, px+1])
    col_map_G = np.nanmean(colmaps_G, axis=0)
    col_map_B = np.nanmean(colmaps_B, axis=0)

    col_map_R[np.isnan(col_map_R)] = 0
    col_map_G[np.isnan(col_map_G)] = 0
    col_map_B[np.isnan(col_map_B)] = 0


    #print(col_map_R[px+1, py+1])
    #print(col_map_G[GAME_OBJECTS["PLAYER"].x+1, GAME_OBJECTS["PLAYER"].y+1])
    #print(col_map_B[GAME_OBJECTS["PLAYER"].x+1, GAME_OBJECTS["PLAYER"].y+1])
    #print(GAME_OBJECTS["PLAYER"].x, GAME_OBJECTS["PLAYER"].y)
    #print(np.shape(col_map_R))
    #print(np.shape(col_map_G))

    return col_map_R, col_map_G, col_map_B, fov_map, int_map

def map_check_creature(x, y, exclude_object = None):

    target = None

    if exclude_object:
        # check object list to find creature at that location that isn't excluded
        for obj in GAME_OBJECTS.values():
            if (obj is not exclude_object and
                obj.x == x and
                obj.y == y and
                obj.creature):
                target = obj

            if target:
                return target

    else:
        # check for any creature on that location
        for obj in GAME_OBJECTS:
            if (obj.x == x and
                obj.y == y and
                obj.creature):
                target = obj

            if target:
                return target

def map_make_escapes(x):
    x = "X"

def select_monsters(LEVEL):
    print("selecting monsters")

    monster_dict = {}
    if LEVEL==1:
        mon_pool = ["SKELETON_1", "SKELETON_2", "SKELETON_3",
                    "MUMMY_3", "MUMMY_2", "MUMMY_3",
                    "ZOMBIE_1", "ZOMBIE_2", "ZOMBIE_3",
                     "SKULL_1"]
        n = 8

    selections = ["NULL"]*n
    i=-1
    while i < n-1:
        sel = random.choice(mon_pool)
        if sel not in selections:
            i+=1
            selections[i] = sel
            #mon_list[i] = sel
            mid = sel.split("_")[0]
            monster = comp_Creature(constants.MONSTER_NAMES[mid],
                                    isplayer=False,
                                    hp=constants.MONSTER_HP[mid],
                                    atk=constants.MONSTER_ATK[mid],
                                    ini=constants.MONSTER_INI[mid],
                                    spd=constants.MONSTER_SPD[mid])

            x, y = helper_random_location()
            monster = obj_Actor(x, y, constants.MONSTER_NAMES[mid], constants.MONSTER_SPRITES[sel], creature=monster, ai=random_walker_AI())
            monster.light = constants.MONSTER_LGT[mid]
            monster.color = constants.MONSTER_COL[mid]
            monster.death_function=death_monster
            GAME_OBJECTS[sel] = monster
            #MONSTERS[i] = monster

    print("monsters_selected")

        #creature_shambSkeleton = comp_Creature("shambling skeleton")
        #SKELETON = obj_Actor(1, 1, "shambling skeleton", constants.S_SKELETON, creature = creature_shambSkeleton, ai=None)
        #creature_mummy = comp_Creature("mummy")
        #MUMMY = obj_Actor(20, 2, "mummy", constants.S_MUMMY, creature = creature_mummy, ai=None)
        #creature_zombie = comp_Creature("zombie", death_function = death_monster)
        #ZOMBIE = obj_Actor(15, 3, "zombie", constants.S_ZOMBIE, creature=creature_zombie, ai=ai_comp_test)

#    ___                    _
#   /   \_ __ __ ___      _(_)_ __   __ _
#  / /\ / '__/ _` \ \ /\ / / | '_ \ / _` |
# / /_//| | | (_| |\ V  V /| | | | | (_| |
#/___,' |_|  \__,_| \_/\_/ |_|_| |_|\__, |
#                                   |___/

def draw_game():

    #global SURFACE_MAIN

    # CLEAR SURFACE
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # DRAW MAP
    draw_map(GAME_MAP)

    # Draw objects
    for obj in GAME_OBJECTS.values():
        obj.draw()

    # draw debug menu
    draw_debug()
    draw_message()
    # UPDATE DISPLAY
    pygame.display.flip()

def draw_map(map_to_draw):
    px = GAME_OBJECTS["PLAYER"].x
    py = GAME_OBJECTS["PLAYER"].y
    rx = -1
    ry = -1
    w = constants.CELL_WIDTH
    h = constants.CELL_HEIGHT
    adj_w = int(constants.SCREEN_WIDTH/2)
    adj_h = int(constants.SCREEN_HEIGHT/2)

    for x in range(px-adj_w,px+adj_w):
        rx+=1
        ry=-1
        for y in range(py-adj_h,py+adj_h):
            ry+=1
            if FOV_MAP[y,x]>0:
                map_to_draw.explored[y,x] = True
                if map_to_draw.walkable[y,x] == False:
                    rgb = (COL_MAP_R[y,x], COL_MAP_G[y,x], COL_MAP_B[y,x])
                    color = constants.COLOR_TORCHLIGHT
                    sprite = constants.S_WALL
                    #sprite.fill(rgb, special_flags=pygame.BLEND_RGB_ADD)
                    filt = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))
                    filt.fill(rgb, special_flags=pygame.BLEND_ADD)
                    #filt.set_alpha(100)
                    filt.set_alpha(180*IMAP[y,x])
                    SURFACE_MAIN.blit(sprite, (rx*w, ry*h))
                    SURFACE_MAIN.blit(filt, (rx*w, ry*h))

                else:
                #    if x==GAME_OBJECTS["PLAYER"].x and y==GAME_OBJECTS["PLAYER"].y:
                        #print(rx*w, ry*h)
                    color = constants.COLOR_TORCHLIGHT
                    rgb = (COL_MAP_R[y,x], COL_MAP_G[y,x], COL_MAP_B[y,x])
                    sprite = constants.S_FLOOR
                    #sprite.fill(rgb, special_flags=pygame.BLEND_RGB_ADD)
                    filt = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))
                    filt.fill(rgb, special_flags=pygame.BLEND_ADD)
                    #filt.set_alpha(100)
                    filt.set_alpha(180*IMAP[y,x])
                    SURFACE_MAIN.blit(sprite, (rx*w, ry*h))
                    SURFACE_MAIN.blit(filt, (rx*w, ry*h))

            elif map_to_draw.explored[y,x]:
                if map_to_draw.walkable[y,x] == False:
                    SURFACE_MAIN.blit(constants.S_WALL_EX, (rx*w, ry*h))
                else:
                    SURFACE_MAIN.blit(constants.S_FLOOR_EX, (rx*w, ry*h))

def draw_debug():

    draw_text(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())), (0, 0), constants.COLOR_WHITE, constants.COLOR_BLACK)
    draw_text(SURFACE_MAIN, "health: " + str(GAME_OBJECTS["PLAYER"].creature.hp), (0, 30), constants.COLOR_RED)
    draw_text(SURFACE_MAIN, "mana: " + str(MANA), (0, 60), constants.COLOR_BLUE)

def draw_message():
    if len(GAME_MESSAGES) <= constants.NUM_MESSAGES:
        to_draw = GAME_MESSAGES
    else:
        to_draw = GAME_MESSAGES[-(constants.NUM_MESSAGES):]
    text_height = helper_text_height(constants.FONT_MESSAGE_TEXT)
    start_y = constants.SCREEN_HEIGHT*constants.CELL_HEIGHT - (constants.NUM_MESSAGES*text_height) - 10

    i = 0
    for message, color in to_draw:
        draw_text(SURFACE_MAIN, message, (0, start_y + (i*text_height)), color)
        i += 1

def draw_text(display_surface, text_to_display, T_coords, text_color, back_color=None):
    # This Function takes in some txt and displays on ref SURFACE

    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)

    text_rect.topleft = T_coords

    display_surface.blit(text_surf, text_rect)

#         __  __    ___  __  __  __
#  /\  /\/__\/ /   / _ \/__\/__\/ _\
# / /_/ /_\ / /   / /_)/_\ / \//\ \
#/ __  //__/ /___/ ___//__/ _  \_\ \
#\/ /_/\__/\____/\/   \__/\/ \_/\__/

def helper_text_objects(incoming_text, incoming_color, incoming_background):

    if incoming_background:
        text_surface = constants.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color, incoming_background)
    else:
        text_surface = constants.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color)

    return text_surface, text_surface.get_rect()

def helper_text_height(font):
    font_object = font.render('a', False, (0, 0, 0))
    font_rect = font_object.get_rect()

    return font_rect.height

def helper_weighted_choice(choices):
    max = sum(choices.values())
    pick = random.uniform(0, max)
    current = 0
    for key, value in choices.items():
        current += value
        if current > pick:
            return key

def helper_random_location():
    #global MONSTERS, PLAYER
    flag_fail=True
    while flag_fail==True:
        flag_fail=True
        x = random.choice(range(GAME_MAP.width))
        y = random.choice(range(GAME_MAP.height))

        if GAME_MAP.walkable[y,x]==True:
            flag_fail=False
            if 'GAME_OBJECTS' in globals():
                for obj in GAME_OBJECTS.values():
                    if obj!="NULL":
                        mx = obj.x
                        my = obj.y
                        if mx==x & my==y:
                            flag_fail=True
    return x, y

def helper_onscreen(px, py, x, y):
    #TODO:
    adj_w = constants.SCREEN_WIDTH/2
    adj_h = constants.SCREEN_HEIGHT/2
    return not (x > px + adj_w or
                x < px - adj_w or
                y > py + adj_h or
                y < py - adj_h)

#   ___
#  / _ \__ _ _ __ ___   ___
# / /_\/ _` | '_ ` _ \ / _ \
#/ /_\\ (_| | | | | | |  __/
#\____/\__,_|_| |_| |_|\___|

def game_initialize():
    #global SURFACE_MAIN, GAME_MAP, GAME_OBJECTS, SKELETON, MUMMY, ZOMBIE, PLAYER, FOV_CALC, CLOCK, GAME_MESSAGES
    global SURFACE_MAIN, GAME_MAP, GAME_OBJECTS, ENEMIES, PLAYER, CLOCK
    global GAME_MESSAGES, LEVEL, TORCH_RADIUS, TURN, MONSTERS, LIGHTSOURCE
    global TORCH_COLOR, MANA, MAGIC_COUNTER, TORCH_COUNTER
    global TURN, COL_MAP_R, COL_MAP_G, COL_MAP_B, FOV_MAP, IMAP
    global GAME_FPS, TURN

    CLOCK = pygame.time.Clock()
    TURN = 0
    TORCH_COUNTER=1
    MAGIC_COUNTER=1
    LEVEL = 1

    TORCH_RADIUS = constants.MAX_TORCH_RADIUS
    MANA = constants.INIT_MANA
    LIGHTSOURCE = "torch"
    TORCH_COLOR = constants.COLOR_TORCHLIGHT

    pygame.init()
    pygame.mouse.set_visible
    pygame.key.set_repeat(50, 1)

    SURFACE_MAIN = pygame.display.set_mode( (constants.SCREEN_WIDTH*constants.CELL_WIDTH, constants.SCREEN_HEIGHT*constants.CELL_HEIGHT) )

    GAME_MESSAGES = []

    creature_player = comp_Creature("Carl the Magnificent",
                                    isplayer=True,
                                    hp=10,
                                    atk=3,
                                    ini=1,
                                    spd=1)

    px = int(constants.MAP_WIDTH/2)
    py = int(constants.MAP_HEIGHT/2)

    GAME_OBJECTS = {}
    GAME_OBJECTS["PLAYER"] = obj_Actor(px, py, "player", constants.S_PLAYER, creature = creature_player, death_function=death_player, light=0)

    print("player initialized")
    #ai_comp_test = test_AI()

    GAME_MAP = map_create()
    print("map created")

    select_monsters(LEVEL)
    print(GAME_OBJECTS)
    print("monsters initialized")
    #GAME_OBJECTS = [PLAYER] + MONSTERS
    print("initialized")

def game_main_loop():
    global TURN, LIGHTSOURCE, TORCH_COUNTER, MAGIC_COUNTER, TORCH_RADIUS, MANA
    global FOV_MAP, IMAP, COL_MAP_R, COL_MAP_G, COL_MAP_B

    game_quit = False

    # definition of action
    player_action = "idle"

    while not game_quit:
        TURN+=1
        if LIGHTSOURCE=="torch":
            TORCH_COUNTER+=1
        elif LIGHTSOURCE=="magic":
            MAGIC_COUNTER+=1

        # player input

        player_action = game_handle_keys()

        if GAME_OBJECTS["PLAYER"].creature.hp < 1:
            time.sleep(5)
            game_quit = True
        if player_action == "QUIT":
            game_quit = True

        elif player_action != "idle":

            for obj in GAME_OBJECTS.values():

                if obj.ai:
                    obj.ai.play_turn()

            if TORCH_COUNTER % constants.TORCH_COUNT_THRESH == 0 and TORCH_RADIUS>1:
                TORCH_RADIUS-=1
                if TORCH_RADIUS==1 and MANA>1:
                    LIGHTSOURCE="magic"
                    TORCH_COLOR=constants.COLOR_MAGICLIGHT
                elif TORCH_RADIUS==1:
                    LIGHTSOURCE="emergency"
                    TORCH_COLOR=constants.COLOR_MAGICLIGHT

            if MAGIC_COUNTER % constants.MANA_COUNT_THRESH == 0 and TORCH_RADIUS>1 and MANA>1:
                MANA-=1
                if MANA<1 and TORCH_RADIUS>1:
                    LIGHTSOURCE="torch"
                    TORCH_COLOR=constants.COLOR_TORCHLIGHT
                elif MANA<1:
                    LIGHTSOURCE="emergency"
                    TORCH_COLOR=constants.COLOR_MAGICLIGHT


        COL_MAP_R, COL_MAP_G, COL_MAP_B, FOV_MAP, IMAP \
         = map_update_fov(GAME_MAP, GAME_OBJECTS["PLAYER"].x,
                                    GAME_OBJECTS["PLAYER"].y)

        draw_game()

        CLOCK.tick(constants.GAME_FPS)

    pygame.quit()
    exit()

def game_handle_keys():
    #TODO get player input
    event_list = pygame.event.get()
    #TODO process input
    for event in event_list:
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                GAME_OBJECTS["PLAYER"].creature.move(0, -1)
                return "moved"
            if event.key == pygame.K_DOWN:
                GAME_OBJECTS["PLAYER"].creature.move(0, 1)
                return "moved"
            if event.key == pygame.K_LEFT:
                GAME_OBJECTS["PLAYER"].creature.move(-1, 0)
                return "moved"
            if event.key == pygame.K_RIGHT:
                GAME_OBJECTS["PLAYER"].creature.move(1, 0)
                return "moved"
            if event.key == pygame.K_t:
                GAME_OBJECTS["PLAYER"].creature.change_torch()
                return "moved"
            if event.key == pygame.K_c:
                print("cast")
                move = GAME_OBJECTS["PLAYER"].creature.cast_spell()
                return move

    return "idle"

def game_message(message_txt, message_color):
        GAME_MESSAGES.append((message_txt, message_color))

if __name__ == '__main__':
    game_initialize()
    game_main_loop()
