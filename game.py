
#   __                          __ _       _     _
#  /__\ ___   __ _ _   _  ___  / /(_) __ _| |__ | |_
# / \/// _ \ / _` | | | |/ _ \/ / | |/ _` | '_ \| __|
#/ _  \ (_) | (_| | |_| |  __/ /__| | (_| | | | | |_
#\/ \_/\___/ \__, |\__,_|\___\____/_|\__, |_| |_|\__|
#            |___/                   |___/

# By Brandt Bessell

import pygame
import pyglet as pyg
import tcod
import constants
import random
import numpy as np
import time
import math

#   ___ _     _           _
#  /___\ |__ (_) ___  ___| |_ ___
# //  // '_ \| |/ _ \/ __| __/ __|
#/ \_//| |_) | |  __/ (__| |_\__ \
#\___/ |_.__// |\___|\___|\__|___/
#          |__/

class obj_Actor:
    def __init__(self, x, y, obj_name, sprite, creature=None, ai=None, light=0, direction="down", color=None, death_function=None):
        self.x = x # map address
        self.y = y # map address
        self.obj_name = obj_name
        self.sprite = sprite
        self.light = light
        self.color = color
        self.death_function = death_function
        self.direction = direction

        self.creature = creature
        if creature:
            self.creature = creature
            creature.owner = self
        self.ai = ai
        if ai:
            self.ai = ai
            ai.owner = self


    def draw(self, Game):
        if self.obj_name=="player":
            #SURFACE_MAIN.blit(self.sprite, (constants.SCREEN_WIDTH/2*constants.CELL_WIDTH, constants.SCREEN_HEIGHT/2*constants.CELL_HEIGHT) )
            sprite = pyg.sprite.Sprite(self.sprite, batch=None)
            sprite.update( (Game.window_width+constants.GUI_WIDTH)//2,
                           Game.window_height//2)
            sprite.draw()
        else:
            if Game.fov[self.y,self.x]>0:
                rx = self.x - Game.game_objects["PLAYER"].x
                ry = self.y - Game.game_objects["PLAYER"].y
                sprite = pyg.sprite.Sprite(self.sprite, batch=None)
                sprite.update( x=(rx*Game.cell_size) + ( (Game.window_width+constants.GUI_WIDTH)//2),
                               y=(ry*Game.cell_size)+(Game.window_height//2) )
                if self.creature.hp<1:
                    sprite.color = (140, 20, 20)
                sprite.draw()
                #SURFACE_MAIN.blit(self.sprite, ( (rx+constants.SCREEN_WIDTH/2)*constants.CELL_WIDTH, (ry+constants.SCREEN_HEIGHT/2)*constants.CELL_HEIGHT) )


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
        if FOV_MAP[self.y,self.x]>0:
            rx = self.x - GAME_OBJECTS["PLAYER"].x
            ry = self.y - GAME_OBJECTS["PLAYER"].y
            if self.shape=="single_target":
                SURFACE_MAIN.blit(self.sprite, ( (rx+constants.SCREEN_WIDTH/2)*constants.CELL_WIDTH, (ry+constants.SCREEN_HEIGHT/2)*constants.CELL_HEIGHT) )


#   ___                                             _
#  / __\___  _ __ ___  _ __   ___  _ __   ___ _ __ | |_ ___
# / /  / _ \| '_ ` _ \| '_ \ / _ \| '_ \ / _ \ '_ \| __/ __|
#/ /__| (_) | | | | | | |_) | (_) | | | |  __/ | | | |_\__ \
#\____/\___/|_| |_| |_| .__/ \___/|_| |_|\___|_| |_|\__|___/
#                     |_|

class comp_Creature:
    #hp,ini,spd,atk)
        def __init__(self, name_personal, isplayer=False, hp=10, ini=1, spd=1,
                     atk=1, mana=0):
                     #death_function = None):
            self.name_personal = name_personal
            self.isplayer = isplayer
            self.hp = hp
            self.maxhp = hp
            self.ini = ini
            self.spd = spd
            self.atk = atk
            self.mana = mana
            #self.death_function = death_function

        def change_torch(self):
            global LIGHTSOURCE, TORCH_COLOR
            #global TORCH_COLOR, TORCH_RADIUS, MAGIC_LIGHT_RADIUS, LIGHTSOURCE
            #global MANA

            if LIGHTSOURCE=="torch" and self.mana > 0:
                LIGHTSOURCE = "magic"
                TORCH_COLOR = constants.COLOR_MAGICLIGHT

            elif LIGHTSOURCE=="magic" and TORCH_RADIUS > 1:
                LIGHTSOURCE = "torch"
                TORCH_COLOR = constants.COLOR_TORCHLIGHT

            else:
                LIGHTSOURCE = "emergency"
                TORCH_COLOR = constants.COLOR_MAGICLIGHT


        def move(self, Game, dx, dy):
            #tile_isWall = (GAME_MAP.walkable[self.owner.y + dy][self.owner.x + dx] == False)
            tile_isWall = (Game.map.walkable[(self.owner.y + dy),(self.owner.x + dx)] == False)

            target = map_check_creature(Game.game_objects, self.owner.x + dx, self.owner.y + dy, self.owner)

            if target:
                self.attack(Game, target, self.atk)

            #new_map = GAME_MAP
            if Game.map.walkable[self.owner.y+dy, self.owner.x+dx] and target is None:
                self.owner.x += dx
                self.owner.y += dy

        def attack(self, Game, target, damage):
            if target.creature.hp < 1:
                Game.game_messages.append((target.creature.name_personal + " is already dead.", constants.COLOR_WHITE))

            else:
                Game.game_messages.append((self.name_personal + " attacks " + target.creature.name_personal + " for " + str(damage) + " damage!", constants.COLOR_WHITE))
                target.creature.take_damage(Game, damage)

        def take_damage(self, Game, damage):
            self.hp -= damage
            Game.game_messages.append((self.name_personal + " HP: " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED))
            if self.hp <= 0:
                #self.death_function=death_monster
                if self.owner.death_function is not None:
                    self.owner.death_function(self.owner, Game)

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
                if objname in Game.game_objects.keys():
                    objname = choice + "_" + str(idx)
                else:
                    pickObj=True
                idx+=1
            pickLoc = False
            w = constants.CELL_WIDTH
            h = constants.CELL_HEIGHT
            hilight_surf = SURFACE_MAIN
            while not pickLoc:
                Game.draw_game()
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
                    adj_w = Game.screen_width//2
                    adj_h = Game.screen_height//2
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
                                Game.game_objects[objname] = new_spell
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
    def play_turn(self, Game):
        #global TURN
        if Game.turn % self.owner.creature.ini == 0:
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
            self.owner.creature.move(Game, x, y)

class dead_AI():
    def play_turn(self, Game):
        return

def death_monster(monster, Game):
    Game.game_messages.append((monster.creature.name_personal + " is dead!", constants.COLOR_RED))
    #monster.creature = None
    monster.ai = dead_AI()
    monster.light = 0
    obname = list(constants.MONSTER_NAMES.keys())[
        list(constants.MONSTER_NAMES.values()).index(monster.obj_name)]
    sprite = constants.MONSTER_DEATH_SPRITES[obname]
    monster.sprite = sprite

def death_player(player, Game):
    Game.game_messages.append( (Game.game_objects["PLAYER"].creature.name_personal + " is dead!", constants.COLOR_RED))
    game_message( "You survived " + str(TURN) + " turns!", constants.COLOR_YELLOW)
    Game.game_objects["PLAYER"].creature.spd = 0

#           _      ___
#  /\/\    /_\    / _ \
# /    \  //_\\  / /_)/
#/ /\/\ \/  _  \/ ___/
#\/    \/\_/ \_/\/


def map_light_intensity(fov_map, radius, obj_x, obj_y):
    for x in range(len(fov_map[0,:])):
        for y in range(len(fov_map[:,0])):
            d = math.sqrt( ( (obj_x-x)*(obj_x-x) + (obj_y-y)*(obj_y-y) ) )
            if d<=radius:
                fov_map[y,x] = fov_map[y,x] * ( (radius/11)**d )
                #fov_map = np.clip(fov_map, 0, 1)



    return fov_map

def map_check_creature(Game_obj, x, y, exclude_object = None):

    target = None

    if exclude_object:
        # check object list to find creature at that location that isn't excluded
        for obj in Game_obj.values():
            if (obj is not exclude_object and
                obj.x == x and
                obj.y == y and
                obj.creature):
                target = obj

            if target:
                return target

    else:
        # check for any creature on that location
        for obj in Game_obj:
            if (obj.x == x and
                obj.y == y and
                obj.creature):
                target = obj

            if target:
                return target

def map_make_escapes(x):
    x = "X"

def select_monsters(LEVEL, game_map, game_objects):
    creature_player = comp_Creature("Carl the Magnificent",
                                    isplayer=True,
                                    hp=constants.INIT_HP,
                                    atk=constants.INIT_ATK,
                                    ini=1,
                                    spd=1,
                                    mana=constants.INIT_MANA)
    game_objects = {}
    px, py, game_objects = helper_random_location(game_map, game_objects)

    game_objects["PLAYER"] = obj_Actor(px, py, "player", constants.A_PLAYER, creature = creature_player, death_function=death_player, light=0)
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

            x, y, game_objects = helper_random_location(game_map, game_objects)
            monster = obj_Actor(x, y, constants.MONSTER_NAMES[mid], constants.MONSTER_SPRITES[sel], creature=monster, ai=random_walker_AI())
            monster.light = constants.MONSTER_LGT[mid]
            monster.color = constants.MONSTER_COL[mid]
            monster.death_function=death_monster
            game_objects[sel] = monster
            #MONSTERS[i] = monster

    print("monsters selected")
    return game_objects

#         __  __    ___  __  __  __
#  /\  /\/__\/ /   / _ \/__\/__\/ _\
# / /_/ /_\ / /   / /_)/_\ / \//\ \
#/ __  //__/ /___/ ___//__/ _  \_\ \
#\/ /_/\__/\____/\/   \__/\/ \_/\__/

def helper_weighted_choice(choices):
    max = sum(choices.values())
    pick = random.uniform(0, max)
    current = 0
    for key, value in choices.items():
        current += value
        if current > pick:
            return key

def helper_random_location(game_map, game_objects):
    #global MONSTERS, PLAYER
    flag_fail=True
    while flag_fail==True:
        flag_fail=True
        x = random.choice(range(game_map.width))
        y = random.choice(range(game_map.height))

        if game_map.walkable[y,x]==True:
            flag_fail=False
            try:
                if not game_objects:
                    pass
                else:
                    for obj in game_objects.values():
                        if obj!="NULL":
                            mx = obj.x
                            my = obj.y
                            if mx==x & my==y:
                                flag_fail=True

            except:
                for obj in game_objects.values():
                    if obj!="NULL":
                        mx = obj.x
                        my = obj.y
                        if mx==x & my==y:
                            flag_fail=True

    return x, y, game_objects

def helper_onscreen(px, py, x, y):
    #TODO:
    adj_w = constants.SCREEN_WIDTH//2
    adj_h = constants.SCREEN_HEIGHT//2
    return not (x > px + adj_w or
                x < px - adj_w or
                y > py + adj_h or
                y < py - adj_h)

def draw_text(text_to_display, x, y, text_color, font_size):
    label = pyg.text.Label(text_to_display, font_name='Dungeon', bold=True,
                           font_size=font_size, color=text_color, x=x, y=y)
    label.draw()

#   ___
#  / _ \__ _ _ __ ___   ___
# / /_\/ _` | '_ ` _ \ / _ \
#/ /_\\ (_| | | | | | |  __/
#\____/\__,_|_| |_| |_|\___|

#@event_loop.event
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

    #pygame.quit()
    event_loop.exit()
    exit()

class Game:

    def __init__(self, window_width, window_height, cell_size, map_width, map_height, map=None, game_objects=None, level=1, light_source="torch"):
        self.turn = 0
        self.game_messages = []
        self.game_messages.append(("Welcome to RogueLight!", constants.COLOR_YELLOW))
        self.window_height = window_height
        self.window_width = window_width
        self.level = level
        self.torch_rad = constants.MAX_TORCH_RADIUS
        self.light_source = light_source
        self.cell_size = cell_size
        self.map = tcod.map.Map(width=map_width, height=map_height)
        self.map.explored = np.full( (map_width, map_height), False, dtype=bool )
        self.map.walkable[:,:] = True
        self.map.isWall = np.full( (map_width, map_height), False, dtype=bool )

        self.map.walkable[:,0:constants.MAP_BUFFER] = False
        self.map.isWall[:,0:constants.MAP_BUFFER] = True
        self.map.walkable[:,(map_width-constants.MAP_BUFFER):map_width] = False
        self.map.isWall[:,(map_width-constants.MAP_BUFFER):map_width] = True
        self.map.walkable[0:constants.MAP_BUFFER,:] = False
        self.map.isWall[0:constants.MAP_BUFFER,:] = True
        self.map.walkable[(map_height-constants.MAP_BUFFER):map_height,:] = False
        self.map.isWall[(map_height-constants.MAP_BUFFER):map_height,:] = True
        self.game_objects = select_monsters(level, self.map, None)
        px = self.game_objects['PLAYER'].x
        py = self.game_objects['PLAYER'].y
        temp = np.array(self.map.walkable)
        temp = tcod.map.compute_fov(self.map.walkable, (py, px), radius=self.torch_rad, algorithm=tcod.FOV_BASIC)
        self.fov = temp
        self.map.red = np.array(self.fov, dtype=int)
        self.map.green = np.array(self.fov, dtype=int)
        self.map.blue = np.array(self.fov, dtype=int)

        self.map_update_fov(px, py)
        self.update = False
        self.draw_map()
        self.draw_gui()
        self.draw_debug()
        self.draw_message()

    def draw_map(self, update=False):
        px = self.game_objects["PLAYER"].x
        py = self.game_objects["PLAYER"].y
        if self.update:
            self.map_update_fov(px, py)
            self.update=False
        rx = -1
        ry = -1
        w = self.cell_size
        h = self.cell_size
        adj_w = (self.window_width-constants.GUI_WIDTH)//(2*self.cell_size)+(constants.GUI_WIDTH//self.cell_size)
        adj_h = self.window_height//(2*self.cell_size)
        batch = pyg.graphics.Batch()
        batch_filt = pyg.graphics.Batch()
        sprites = []
        for x in range(px-adj_w,px+adj_w):
            rx+=1
            ry=-1
            for y in range(py-adj_h,py+adj_h):
                ry+=1
                if self.fov[y,x]>0:
                    self.map.explored[y,x] = True
                    if self.map.walkable[y,x] == False:
                        rgb = (self.map.red[y,x], self.map.green[y,x], self.map.blue[y,x])
                        color = constants.COLOR_TORCHLIGHT
                        sprite = pyg.sprite.Sprite(constants.S_WALL, batch=batch)
                        sprite.color = constants.COLOR_WALL
                        sprite.update(x=rx*w, y=ry*h)
                        filt = pyg.sprite.Sprite(constants.S_FILT, batch=batch_filt)
                        filt.update(x=rx*w, y=ry*h)
                        filt.color = rgb
                        filt.opacity = 180*self.map.lum[y,x]
                        if filt.opacity>250 : filt.opacity=250
                        sprites.append(sprite)
                        sprites.append(filt)
                    else:
                        color = constants.COLOR_TORCHLIGHT
                        rgb = (self.map.red[y,x], self.map.green[y,x], self.map.blue[y,x])
                        sprite = pyg.sprite.Sprite(constants.S_FLOOR, batch=batch)
                        sprite.color = constants.COLOR_WALL
                        sprite.update(x=rx*w, y=ry*h)
                        filt = pyg.sprite.Sprite(constants.S_FILT, batch=batch_filt)
                        filt.update(x=rx*w, y=ry*h)
                        filt.color = rgb
                        filt.opacity = 180*self.map.lum[y,x]
                        if filt.opacity>250 : filt.opacity=250
                        sprites.append(sprite)
                        sprites.append(filt)

                elif self.map.explored[y,x]:
                    if self.map.walkable[y,x] == False:
                        rgb = (self.map.red[y,x], self.map.green[y,x], self.map.blue[y,x])
                        sprite = pyg.sprite.Sprite(constants.S_WALL_EX, batch=batch)
                        sprite.update(x=rx*w, y=ry*h)
                        sprite.color = constants.COLOR_WALL
                        filt = pyg.sprite.Sprite(constants.S_FILT, batch=batch_filt)
                        filt.update(x=rx*w, y=ry*h)
                        filt.color = (0,0,0)
                        filt.opacity = 180*self.map.lum[y,x]
                        if filt.opacity>250 : filt.opacity=250
                        sprites.append(sprite)
                        sprites.append(filt)
                    else:
                        rgb = (self.map.red[y,x], self.map.green[y,x], self.map.blue[y,x])
                        sprite = pyg.sprite.Sprite(constants.S_FLOOR_EX, batch=batch)
                        sprite.update(x=rx*w, y=ry*h)
                        sprite.color = constants.COLOR_WALL
                        filt = pyg.sprite.Sprite(constants.S_FILT, batch=batch_filt)
                        filt.update(x=rx*w, y=ry*h)
                        filt.color = (0,0,0)
                        filt.opacity = 180*self.map.lum[y,x]
                        if filt.opacity>250 : filt.opacity=250
                        #SURFACE_MAIN.blit(constants.S_FLOOR_EX, (rx*w, ry*h))
                        sprites.append(sprite)
                        sprites.append(filt)
        batch.draw()
        batch_filt.draw()
        self.game_objects['PLAYER'].draw(self)
        for obj in self.game_objects.values():
            if obj.obj_name != "player":
                obj.draw(self)

    def map_update_fov(self, px, py):
        colmaps_R = []
        colmaps_G = []
        colmaps_B = []
        if self.light_source=="torch":
            rad = self.torch_rad
            torch_col = constants.COLOR_TORCHLIGHT
        elif self.light_source=="magic":
            rad = constants.MAGIC_LIGHT_RADIUS
            torch_col = constants.COLOR_MAGICLIGHT
        elif self.light_source=="emergency":
            rad = constants.E_LIGHT_RADIUS
            torch_col = constants.COLOR_MAGICLIGHT

        fov_map = tcod.map.compute_fov(self.map.walkable, (py, px),
                                       radius=rad, algorithm=tcod.FOV_SHADOW)

        int_map = tcod.map.compute_fov(self.map.walkable, (py, px),
                                       radius=rad, algorithm=tcod.FOV_SHADOW)

        fov_map = np.array(fov_map, dtype=np.float16)
        int_map = np.array(int_map, dtype=np.float16)
        int_map = \
        map_light_intensity(int_map, rad, px, py)
        col_R = (fov_map*torch_col[0])
        col_G = (fov_map*torch_col[1])
        col_B = (fov_map*torch_col[2])
        col_R[col_R==0] = np.nan
        col_G[col_G==0] = np.nan
        col_B[col_B==0] = np.nan
        colmaps_R.append(col_R)
        colmaps_G.append(col_G)
        colmaps_B.append(col_B)

        for obj in self.game_objects.values():
            if obj.light>0:
                fmap = tcod.map.compute_fov(self.map.walkable, (obj.y, obj.x),
                                 radius=obj.light, algorithm=tcod.FOV_SHADOW)

                fmap = np.array(fmap, dtype=np.float16)
                imap = tcod.map.compute_fov(self.map.walkable, (obj.y, obj.x),
                                 radius=obj.light, algorithm=tcod.FOV_SHADOW)

                imap = np.array(imap, dtype=np.float16)
                int_map += map_light_intensity(imap, obj.light, obj.x, obj.y)
                fov_map += fmap
                col_R = (fmap*obj.color[0])
                col_G = (fmap*obj.color[1])
                col_B = (fmap*obj.color[2])
                min_col = constants.COLOR_CLIP
                col_R[col_R==0] = np.nan
                col_G[col_G==0] = np.nan
                col_B[col_B==0] = np.nan
                colmaps_R.append(col_R)
                colmaps_G.append(col_G)
                colmaps_B.append(col_B)

        col_map_R = np.nanmean(colmaps_R, axis=0)
        col_map_G = np.nanmean(colmaps_G, axis=0)
        col_map_B = np.nanmean(colmaps_B, axis=0)
        col_map_R[np.isnan(col_map_R)] = 0
        col_map_G[np.isnan(col_map_G)] = 0
        col_map_B[np.isnan(col_map_B)] = 0
        self.map.lum = int_map
        self.map.red = col_map_R
        self.map.green = col_map_G
        self.map.blue = col_map_B
        self.fov = fov_map
        return

    def draw_gui(self):
        batch = pyg.graphics.Batch()
        background = pyg.shapes.Rectangle(0, 0, constants.GUI_WIDTH, self.window_height,
                                          color=constants.COLOR_GREY, batch=batch)

        batch.draw()

    def draw_objects(self):
        for obj in self.game_objects.values():
            obj.draw(self)

    def draw_debug(self):
        start_y = 5
        #draw_text("fps: " + str(int(CLOCK.get_fps())), (0, 0), constants.COLOR_WHITE, constants.COLOR_BLACK)
        draw_text("health: " + str(self.game_objects["PLAYER"].creature.hp), 5, self.window_height-28-start_y, constants.COLOR_RED, 28)
        draw_text("mana: " + str(self.game_objects["PLAYER"].creature.mana), 150, self.window_height-28-start_y, constants.COLOR_BLUE, 28)

    def draw_message(self):
        if len(self.game_messages) <= constants.NUM_MESSAGES:
            to_draw = self.game_messages
        else:
            to_draw = self.game_messages[-(constants.NUM_MESSAGES):]
        #text_height = helper_text_height(constants.FONT_MESSAGE_TEXT)
        text_height = 32
        start_y = 0

        i = 0
        for message, color in to_draw[::-1]:
            draw_text(message, 5, start_y + (i*text_height), color, 28)
            i += 1
