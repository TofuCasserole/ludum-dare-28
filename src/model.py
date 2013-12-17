'''
Created on Dec 13, 2013

@author: thedoctor
'''
MnM = 0
MnM_RANGED = 1
BOSS=2

boss_types = [2]

MONSTER_IMAGES = ['mnm.png', 'green_mnm.png','mnm.png']

EAST = "east"
WEST = "west"
NORTH = "north"
SOUTH = "south"

LENGTH = 9
WIDTH = 13

import actor
import os
import random
import pygame
import main
import behaviors
import monsters
import utils
from pygame.locals import *

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('../', 'res', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
    return image

class Character(actor.Actor):
    def __init__(self):
        image = load_png('char.png')
        image = pygame.transform.scale(image, (26, 26))
        actor.Actor.__init__(self, image, image.get_rect(), None, False, True)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.health = 100
        #self.room = start_room
        self.movepos = [0,0]
        self.tryingmoveright = False
        self.tryingmoveleft = False
        self.tryingmoveup = False
        self.tryingmovedown = False
        self.last_direction_moved = "right"
        self.state = "move"
        self.hitcount = 0
        self.invuln_count = 0
        self.hitmove = [0,0]
        self.sword_cooldown = 30
        self.rect.midleft = self.area.midleft
        self.rect = self.rect.move([74,0])
        self.cannot_collide = pygame.sprite.Group()
        self.rune_effects = [False, False, False, False, False, False, False, False]
        self.buff_effects = [False, False, False, False, False, False, False, False]
    
    def getmovepos(self):
        if self.state == "hit":
            return self.hitmove
        else:
            return self.movepos
        
    def on_collision(self, sprite):
        if self.state == "move" and isinstance(sprite, monsters.Monster):
            self.health -= sprite.strength
            if self.rune_effects[1]:
                print("taking 20% damage")
                self.health += sprite.strength*4/5
        
    def update(self, obstacles, moveables, sword):
        if self.rune_effects[0]:
            self.health = 100
            self.rune_effects[0] = False
            
        if self.rune_effects[3]:
            for moveable in moveables:
                if moveable != self and utils.distance(self.rect.center, moveable.rect.center) <= 200:
                    moveable.health -= 60
                    if moveable.health < 0:
                        moveable.kill()
                        if moveable.isBoss:
                            pygame.event.post(pygame.event.Event(USEREVENT, {'subtype': 'BossDeath'}))
                        else:
                            pygame.event.post(pygame.event.Event(USEREVENT, {'subtype': 'MonsterDeath'}))
                        
            self.rune_effects[3] = False
                    
        
        self.sword_cooldown += 1
        if self.state == "hit":
            if self.hitcount < 5:
                self.hitcount += 1
            else:
                self.state = "invulnerable"
                self.hitcount = 0
                for current_collisions in pygame.sprite.spritecollide(self, moveables,0):
                    self.cannot_collide.add(current_collisions)
            move(self, [], obstacles, self.getmovepos())
            pygame.event.pump()
            return
        
        if self.state == "invulnerable":
            if self.invuln_count < 10:
                self.invuln_count += 1
            else:
                self.invuln_count = 0
                self.state = "move"
        
        if sword.sprites() == []:
            move(self, moveables, obstacles, self.getmovepos())
        for current_collision in self.cannot_collide.sprites():
            if not current_collision in pygame.sprite.spritecollide(self, moveables, 0):
                self.cannot_collide.remove(current_collision)
        if self.rect.right < 32 or self.rect.left > 608 or self.rect.bottom < 32 or self.rect.top > 448:
            self.rect.center = self.area.center
        pygame.event.pump()
        

#class Monster(pygame.sprite.Sprite):
#    def __init__(self, type, behavior, isBoss=False):
#        self.behavior = behavior
#        pygame.sprite.Sprite.__init__(self)
#        self.image = load_png(MONSTER_IMAGES[type])
#        self.image = pygame.transform.scale2x(self.image)
#        self.rect = self.image.get_rect()
#        screen = pygame.display.get_surface()
#        self.area = screen.get_rect()
#        random.seed()
#        self.state = "chase"
#        self.movepos = [0,0]
#        self.hitcount = 0
#        self.pushcount = 0
#        self.cannot_collide = pygame.sprite.Group()
#        self.isBoss=isBoss
#        self.type = type
#        if type == MnM:
#            self.health = 20
#            self.strength = 2
#            self.movecount = 0
#            self.waitcount = 0
#        if type == MnM_RANGED:
#            self.health = 20
#            self.strength = 2
#            self.waitcount = 0
#            self.movecount = 0
#            x = random.randint(0,2)
#            if x == 0:
#                self.state = "wait2"
#                self.waitcount = random.randint(0,40)
#            if x == 1:
#                self.state = "move"
#                self.movepos[0] = random.randint(-1,1)*3
#                self.movepos[1] = random.randint(-1,1)*3
#                self.movecount = random.randint(0,60)
#            if x == 2:
#                self.state = "wait1"
#                self.waitcount = random.randint(0,40)
#        if type==BOSS:
#            self.health=50
#            self.strength=5
#            self.state='wait' 
#            self.waitcount = 0
#            self.movecount = 0
#   def getmovepos(self):
#        return self.movepos
# class Monster(pygame.sprite.Sprite):
#     def __init__(self, type, behavior, isBoss=False):
#         self.behavior = behavior
#         pygame.sprite.Sprite.__init__(self)
#         self.image = load_png(MONSTER_IMAGES[type])
#         self.image = pygame.transform.scale2x(self.image)
#         self.rect = self.image.get_rect()
#         screen = pygame.display.get_surface()
#         self.area = screen.get_rect()
#         random.seed()
#         self.state = "chase"
#         self.movepos = [0,0]
#         self.hitcount = 0
#         self.pushcount = 0
#         self.cannot_collide = pygame.sprite.Group()
#         self.isBoss=isBoss
#         self.type = type
#         if type == MnM:
#             self.health = 20
#             self.strength = 2
#         if type == MnM_RANGED:
#             self.health = 20
#             self.strength = 2
#             self.waitcount = 0
#             self.movecount = 0
#             x = random.randint(0,2)
#             if x == 0:
#                 self.state = "wait2"
#                 self.waitcount = random.randint(0,40)
#             if x == 1:
#                 self.state = "move"
#                 self.movepos[0] = random.randint(-1,1)*3
#                 self.movepos[1] = random.randint(-1,1)*3
#                 self.movecount = random.randint(0,60)
#             if x == 2:
#                 self.state = "wait1"
#                 self.waitcount = random.randint(0,40)
#         if type==BOSS:
#             self.health=50
#             self.strength=5
#             self.state='wait' 
#             self.waitcount = 0
#             self.movecount = 0
#     def getmovepos(self):
#         return self.movepos
#     
#     def on_collision(self, sprite):
#         if isinstance(sprite, Character):
#             if (sprite.state == "move"):
#                 sprite.hitmove[0] = self.movepos[0]/3*8
#                 sprite.hitmove[1] = self.movepos[1]/3*8
#                 sprite.state = "hit"
#             if (self.state != "hit"):
#                 self.movepos[0] = 0
#                 self.movepos[1] = 0
#                 self.state = "hit"
#         '''if isinstance(sprite, Monster):
#             if (self.state == "hit" and sprite.state != "hit"):
#                 sprite.movepos[0] = self.movepos[0]
#                 sprite.movepos[1] = self.movepos[1]
#                 sprite.state = "hit"
#                 sprite.hitcount = self.hitcount''' 
#     
#     def update(self, obstacles, moveables, character):
#         self.behavior(self, obstacles, moveables, character)
#         if (self.rect.bottom < 32 or self.rect.top > 448 or
#             self.rect.right < 64 or self.rect.bottom > self.rect.left > 608):
#             if not self.type in boss_types:
#                 self.kill()
#                 pygame.event.post(pygame.event.Event(USEREVENT, {'subtype': 'MonsterDeath'}))
#             else:
#                 self.rect.center = self.area.center
    

class Projectile(actor.Actor):
    def __init__(self, image, strength):
        image = load_png(image)
        image = pygame.transform.scale(image, (16, 16))
        actor.Actor.__init__(self, image, image.get_rect(), None, False, False)
        self.strength = strength
        self.movepos = [0,0]
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.cannot_collide = pygame.sprite.Group()
        
    def on_collision(self, sprite):
        if sprite.state != "invulnerable" and sprite.state != "hit":
            sprite.health -= self.strength
            self.kill()
        
    def update(self, charactersprites):
        move(self, charactersprites, [], self.movepos)
        for sprite in charactersprites.sprites():
            if pygame.sprite.spritecollide(self, sprite.currentroom.obstacles, 0):
                self.kill()
        if not self.area.contains(self):
            self.kill()
        pygame.event.pump()


class Sword(pygame.sprite.Sprite):
    def __init__(self, character):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('sword.png')
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rotate = 90
        self.strength = 7
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        if character.last_direction_moved == "right":
            self.image = pygame.transform.rotate(self.image, 270-self.rotate)
            self.rotate = 270
            self.rect.midleft = character.rect.midright
        if character.last_direction_moved == "left":
            self.image = pygame.transform.rotate(self.image, 90-self.rotate)
            self.rotate = 90
            self.rect.midright = character.rect.midleft
        if character.last_direction_moved == "up":
            self.image = pygame.transform.rotate(self.image, 0-self.rotate)
            self.rotate = 0
            self.rect.midbottom = character.rect.midtop
        if character.last_direction_moved == "down":
            self.image = pygame.transform.rotate(self.image, 180-self.rotate)
            self.rotate = 180
            self.rect.midtop = character.rect.midbottom
        self.count = 0
        
    def update(self, character, monsters):
        if self.count > 5:
            self.kill()
            character.sword_cooldown = 0
            return
        if character.last_direction_moved == "right":
            self.image = pygame.transform.rotate(self.image, 270-self.rotate)
            self.rotate = 270
            self.rect.midleft = character.rect.midright
        if character.last_direction_moved == "left":
            self.image = pygame.transform.rotate(self.image, 90-self.rotate)
            self.rotate = 90
            self.rect.midright = character.rect.midleft
        if character.last_direction_moved == "up":
            self.image = pygame.transform.rotate(self.image, 0-self.rotate)
            self.rotate = 0
            self.rect.midbottom = character.rect.midtop
        if character.last_direction_moved == "down":
            self.image = pygame.transform.rotate(self.image, 180-self.rotate)
            self.rotate = 180
            self.rect.midtop = character.rect.midbottom
        for monster in pygame.sprite.spritecollide(self, monsters, 0):
            monster.state = "pushback"
            monster.health -= self.strength
            if character.rune_effects[2]:
                monster.health -= self.strength*3
                print "Weapon dealt quadruple damage"
            if monster.health <= 0:
                if character.buff_effects[0]:
                    character.health += 5
                monster.kill()
                if monster.isBoss:
                    pygame.event.post(pygame.event.Event(USEREVENT, {'subtype': 'BossDeath'}))
                else:
                    pygame.event.post(pygame.event.Event(USEREVENT, {'subtype': 'MonsterDeath'}))
            if character.last_direction_moved == "right":
                monster.rect.left = self.rect.right
                monster.movepos = [16, 0]
            elif character.last_direction_moved == "left":
                monster.rect.right = self.rect.left
                monster.movepos = [-16, 0]
            elif character.last_direction_moved == "down":
                monster.rect.top = self.rect.bottom
                monster.movepos = [0, 16]
            elif character.last_direction_moved == "up":
                monster.rect.bottom = self.rect.top
                monster.movepos = [0, -16]
        self.count += 1

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, location, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png(sprite)
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
    
        self.rect.topleft = location

class Door(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('char.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        
    def update(self, character, l):
        if pygame.sprite.collide_mask(self, character):
            if self.rect.left == 320 and self.rect.top == 0:
                character.rune_effects = [False, False, False, False, False, False, False, False]
                character.rect.y = 416
                character.currentroom.moveables.remove(character)
                character.currentroom = l.getLocation(character.currentroom.connectingRooms['north'])
                character.currentroom.moveables.add(character)
            elif self.rect.left == 320 and self.rect.top == 448:
                character.rune_effects = [False, False, False, False, False, False, False, False]
                character.rect.y = 32                
                character.currentroom.moveables.remove(character)
                character.currentroom = l.getLocation(character.currentroom.connectingRooms['south'])
                character.currentroom.moveables.add(character)
            elif self.rect.top == 224 and self.rect.left == 32:
                character.rune_effects = [False, False, False, False, False, False, False, False]
                character.rect.x = 576
                character.currentroom.moveables.remove(character)
                character.currentroom = l.getLocation(character.currentroom.connectingRooms['west'])
                character.currentroom.moveables.add(character)
            elif self.rect.top == 224 and self.rect.left == 608:
                character.rune_effects = [False, False, False, False, False, False, False, False]
                character.rect.x = 64
                character.currentroom.moveables.remove(character)
                character.currentroom = l.getLocation(character.currentroom.connectingRooms['east'])
                character.currentroom.moveables.add(character)
        for monster in pygame.sprite.spritecollide(self, character.currentroom.monsters, 0):
            if self.rect.left == 320 and self.rect.top == 0:
                monster.rect.top = self.rect.bottom
            elif self.rect.left == 320 and self.rect.top == 448:
                monster.rect.bottom = self.rect.top
            elif self.rect.top == 224 and self.rect.left == 32:
                monster.rect.left = self.rect.right
            elif self.rect.top == 224 and self.rect.left == 608:
                monster.rect.right = self.rect.left

class MedBay(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('medbay.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.topleft = (576,416)
        self.can_heal = False
        self.health = 25
        
    def update(self, character, level):
        if pygame.sprite.collide_rect(self, character) and self.health > 0 and character.health < 100:
            self.can_heal = True
        else:
            self.can_heal = False
            self.is_healing = False
        if self.is_healing:
            self.health -= .25
            character.health += .25
            level.health -= .25
                
class BossDoor(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('bossdoor.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        
    def update(self, moveables):
        for sprite in pygame.sprite.spritecollide(self, moveables, 0):
            if self.rect.left == 320 and self.rect.top == 0:
                sprite.rect.top = self.rect.bottom
            elif self.rect.left == 320 and self.rect.top == 448:
                sprite.rect.bottom = self.rect.top
            elif self.rect.top == 224 and self.rect.left == 32:
                sprite.rect.left = self.rect.right
            elif self.rect.top == 224 and self.rect.left == 608:
                sprite.rect.right = self.rect.left
'''
doors are passed as an array of "east", "north", "south", and "west"

obstacles are passed as a list array of 2 tuples with the y parameter first and the x
aparameter second, starting at 0,0 in the top left corner e.g.,
-------------------
| 0,0 | 0,1 s| 0,2 |
-------------------
| 1,0 | 1,1 | 1,2 |
-------------------
| 2,0 | 2,1 | 2,2 |
-------------------

unlocated monster objects are passed as an array on construction
'''
random.seed()

def move(sprite, moveables, obstacles, movepos, realign = False):
    newpos = sprite.rect.move([movepos[0], 0])
    if not realign:
        sprite.rect = newpos
    for obstacle in pygame.sprite.spritecollide(sprite, obstacles, 0):
        if movepos[0] > 0 and sprite.rect.right > obstacle.rect.left:
            sprite.rect.right = obstacle.rect.left
            for moveable in pygame.sprite.spritecollide(sprite, moveables, 0):
                if moveable == sprite:
                    continue
                move(moveable, moveables, obstacles, moveable.getmovepos(), True)
        if movepos[0] < 0 and sprite.rect.left < obstacle.rect.right:
            sprite.rect.left = obstacle.rect.right
            for moveable in pygame.sprite.spritecollide(sprite, moveables, 0):
                if moveable == sprite:
                    continue
                move(moveable, moveables, obstacles, moveable.getmovepos(), True)
    for moveable in pygame.sprite.spritecollide(sprite, moveables, 0):
        if moveable == sprite:
            continue
        if movepos[0] > 0 and sprite.rect.right > moveable.rect.left:
            if not sprite.cannot_collide.has(moveable) and not moveable.cannot_collide.has(sprite):
                sprite.rect.right = moveable.rect.left
            sprite.on_collision(moveable)
            moveable.on_collision(sprite)
            for moveable2 in pygame.sprite.spritecollide(sprite, moveables, 0):
                if moveable2 == sprite:
                    continue
                move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
        if movepos[0] < 0 and sprite.rect.left < moveable.rect.right:
            if not sprite.cannot_collide.has(moveable) and not moveable.cannot_collide.has(sprite):
                sprite.rect.left = moveable.rect.right
            sprite.on_collision(moveable)
            moveable.on_collision(sprite)
            for moveable2 in pygame.sprite.spritecollide(sprite, moveables, 0):
                if moveable2 == sprite:
                    continue
                move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
    newpos = sprite.rect.move([0, movepos[1]])
    if not realign:
        sprite.rect = newpos
    for obstacle in pygame.sprite.spritecollide(sprite, obstacles, 0):
        if movepos[1] > 0 and sprite.rect.bottom > obstacle.rect.top:
            sprite.rect.bottom = obstacle.rect.top
            for moveable in pygame.sprite.spritecollide(sprite, moveables, 0):
                if moveable == sprite:
                    continue
                move(moveable, moveables, obstacles, moveable.getmovepos(), True)
        if movepos[1] < 0 and sprite.rect.top < obstacle.rect.bottom:
            sprite.rect.top = obstacle.rect.bottom
            for moveable in pygame.sprite.spritecollide(sprite, moveables, 0):
                if moveable == sprite:
                    continue
                move(moveable, moveables, obstacles, moveable.getmovepos(), True)
    for moveable in pygame.sprite.spritecollide(sprite, moveables, 0):
        if moveable == sprite:
            continue
        if movepos[1] > 0 and sprite.rect.bottom > moveable.rect.top:
            if not sprite.cannot_collide.has(moveable) and not moveable.cannot_collide.has(sprite):
                sprite.rect.bottom = moveable.rect.top
            sprite.on_collision(moveable)
            moveable.on_collision(sprite)
            for moveable2 in pygame.sprite.spritecollide(sprite, moveables, 0):
                if moveable2 == sprite:
                    continue
                move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
        if movepos[1] < 0 and sprite.rect.top < moveable.rect.bottom:
            if not sprite.cannot_collide.has(moveable) and not moveable.cannot_collide.has(sprite):
                sprite.rect.top = moveable.rect.bottom
            sprite.on_collision(moveable)
            moveable.on_collision(sprite)
            for moveable2 in pygame.sprite.spritecollide(sprite, moveables, 0):
                if moveable2 == sprite:
                    continue
                move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)


class Room:
    def __init__(self, cord, doors=[], obstacles=None, monsters=None):
        self.doors = doors
        self.connectingRooms={}#door:room -> NORTH:<roomObject>
        self.obstacles = pygame.sprite.RenderUpdates()
        self.monsters = pygame.sprite.RenderUpdates()
        self.moveables = pygame.sprite.RenderUpdates()
        self.walls = pygame.sprite.RenderUpdates()
        self.door_sprites = pygame.sprite.RenderUpdates()
        self.projectiles = pygame.sprite.RenderUpdates()
        self.bossdoors = pygame.sprite.RenderUpdates()
        self.medbay = pygame.sprite.RenderUpdates()
        self.cord=cord
        
    def add_monsters(self, charactersprites, level):
        if level.bossRoom==self.cord:
            temp_monster = monsters.Monster(monsters.BOSS)
            temp_monster.rect.topleft = (random.randint(32,temp_monster.area.right-32), random.randint(0,temp_monster.area.bottom-32))
            while (pygame.sprite.spritecollide(temp_monster, charactersprites, 0) != [] or pygame.sprite.spritecollide(temp_monster, self.walls, 0) != []
               or pygame.sprite.spritecollide(temp_monster, self.monsters, 0) != []):
                    temp_monster.rect.topleft = (random.randint(0,temp_monster.area.right), random.randint(0,temp_monster.area.bottom))
            self.monsters.add(temp_monster)
            self.moveables.add(self.monsters)
            return
        for i in range(random.randint(3,5)):
            x = random.randint(0,1)
            if x == 0:
                temp_monster = monsters.Monster(monsters.MNM)
            if x == 1:
                temp_monster = monsters.Monster(monsters.MNM_RANGED)
            temp_monster.rect.topleft = (random.randint(32,temp_monster.area.right-64), random.randint(0,temp_monster.area.bottom-64))
            while (pygame.sprite.spritecollide(temp_monster, charactersprites, 0) != [] or pygame.sprite.spritecollide(temp_monster, self.walls, 0) != []
               or pygame.sprite.spritecollide(temp_monster, self.monsters, 0) != []):
                    temp_monster.rect.topleft = (random.randint(0,temp_monster.area.right), random.randint(0,temp_monster.area.bottom))
            self.monsters.add(temp_monster)
        level.num_monsters += len(self.monsters.sprites())
        self.moveables.add(self.monsters)
        
  
    def generateWalls(self, level):
        #print(self.doors)
        if self.obstacles!=None and self.monsters!=None:
            possible_locations = [(x,y) for x in range(0, WIDTH) for y in range (0, LENGTH) if (x,y) not in self.obstacles]
            random.shuffle(possible_locations)
            for monster in self.monsters:
                monster.location = possible_locations.pop()
        self.walls = pygame.sprite.RenderPlain()
        # generate north/south walls
        for x in range(32, 640, 32):
            if not (x == 320 and NORTH in self.connectingRooms):
                self.walls.add(Obstacle((x, 0), "wall.png"))
            else:
                myDoor = Door((320,0))
                self.door_sprites.add(myDoor)
                if level.bossRoom == (self.cord[0], self.cord[1]-1):
                    self.door_sprites.remove(myDoor)
                    self.bossdoors.add(BossDoor((320,0)))
            if not (x == 320 and SOUTH in self.connectingRooms):
                self.walls.add(Obstacle((x, 448), "wall.png"))
            else:
                myDoor = Door((320,448))
                self.door_sprites.add(myDoor)
                if level.bossRoom == (self.cord[0], self.cord[1]+1):
                    self.door_sprites.remove(myDoor)
                    self.bossdoors.add(BossDoor((320,448)))
        # generate east/west walls
        for y in range(0, 480, 32):
            if not (y == 224 and WEST in self.connectingRooms):
                self.walls.add(Obstacle((32, y), "wall.png"))
            else:
                myDoor = Door((32,224))
                self.door_sprites.add(myDoor)
                if level.bossRoom == (self.cord[0]-1, self.cord[1]):
                    self.door_sprites.remove(myDoor)
                    self.bossdoors.add(BossDoor((32,224)))
            if not (y == 224 and EAST in self.connectingRooms):
                self.walls.add(Obstacle((608, y), "wall.png"))
            else:
                myDoor = Door((608,224))
                self.door_sprites.add(myDoor)
                if level.bossRoom == (self.cord[0]+1, self.cord[1]):
                    self.door_sprites.remove(myDoor)
                    self.bossdoors.add(BossDoor((608,224)))

    def monster_locations(self):
        return [monster.location for monster in self.monsters]
    

cur_room_row = 0
cur_room_col = 0


class Level:
    def __init__(self,levelNumber, debug=False):
        if not debug:
            self.SIZE=10
            self.levelGrid=[[-1]*self.SIZE for x in range(self.SIZE)]
            self.levelNumber=levelNumber
            self.numberOfRooms=random.randint(10,15)
            self.rootRoom=(self.SIZE/2,self.SIZE/2)
            self.generateLevel()
            self.bossRoom=self.findLongestPath(self.rootRoom)
            self.generateWalls()
            self.printGrid()
            self.generateObstacles()
            self.addmedbay()
            self.num_monsters = 0
            self.health = 25
    def addmedbay(self):
        mylist = [i for i in self.getAllRooms() if i.cord != self.bossRoom]
        random.shuffle(mylist)
        mylist.pop().medbay.add(MedBay())
    def generateWalls(self):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if isinstance(self.levelGrid[i][j],Room):
                    self.levelGrid[i][j].generateWalls(self)
    def getLocation(self, gridCords):
        return self.levelGrid[gridCords[0]][gridCords[1]]
    def getAllRooms(self):
        list = []
        for y in self.levelGrid:
            for x in y:
                if x != -1:
                    list.append(x)
        return list

    def generateLevel(self):
        direction={0:NORTH,1:EAST,2:SOUTH,3:WEST}
        inverseDirection={0:SOUTH,1:WEST,2:NORTH,3:EAST}
        start=(self.SIZE/2,self.SIZE/2)
        self.levelGrid[start[0]][start[1]]=Room(start)
        count=1
        currentPlace=start
        queue=[]
        while count<self.numberOfRooms:
            #print currentPlace[0]
            currentX=currentPlace[0]
            currentY=currentPlace[1]
            #generate some exits
            exits=self.generateExits(currentPlace)
            #print("Current Room:", currentPlace)
            for i in range(4):
                if exits[i]==-1:
                    continue
                x=exits[i][0]
                y=exits[i][1]
                if self.levelGrid[x][y]==-1:
                    self.levelGrid[x][y]=Room(exits[i])
                    queue.append(exits[i])
                    count+=1
                #add the room to the connectedrooms dict
                self.levelGrid[currentX][currentY].connectingRooms[direction[i]]=exits[i]
                self.levelGrid[x][y].connectingRooms[inverseDirection[i]]=currentPlace
            #now we need to goto the next place in the queue, if its empty idk what we are going to do..
            
            self.levelGrid[currentX][currentY].doors = []
            for room in self.levelGrid[currentX][currentY].connectingRooms:
                self.levelGrid[currentX][currentY].doors.append(room)
            #print "Neighbors:", self.levelGrid[currentX][currentY].doors
            if len(queue)>0:
                currentPlace=queue.pop(0)
            else:
                #gotta do something here...
                pass
    def generateExits(self, position):
        newRooms=[-1,-1,-1,-1]
        for i in range(4):
            if bool(random.randint(0,1)):
                if i==0:#north
                    newRooms[i]=(position[0],position[1]-1)
                elif i==1:#east
                    newRooms[i]=(position[0]+1,position[1])
                elif i==2:#south
                    newRooms[i]=(position[0],position[1]+1)
                elif i==3:#west
                    newRooms[i]=(position[0]-1,position[1])
        #time to check the new rooms to make sure that they are in range etc
        for i in range(3,-1,-1):
            if newRooms[i]!=-1:
                x=newRooms[i][0]
                y=newRooms[i][1]
                if x>=self.SIZE or x<0:
                    newRooms[i]=-1
                    continue
                if y>=self.SIZE or y<0:
                    newRooms[i]=-1
                    continue
                #now check to see if this room butts up against anything existing room
                if self.levelGrid[x][y]!=-1:
                    #lets see if we want to connect them
                    if not bool(random.randint(0,1)):
                        newRooms[i]=-1
                        continue
        #print(newRooms)
        return newRooms
    def findLongestPath(self, startingPos):
        #we need to populate the queue and get going!
        queue=[]
        queue.append([startingPos, 0])
        longest=self.__longestPath(queue,[],[])  
        return longest[0]
    def __longestPath(self, queue, visited, longest):
        if len(queue)==0:
            return longest
        #pop the first element
        currentPos=queue.pop(0)
        if currentPos[0] in visited:
            #lets dump this one and move on
            return self.__longestPath(queue, visited, longest)
        #check the current node to see if it is the longest
        if len(longest)==0:
            longest=currentPos
        elif currentPos[1]>longest[1]:
            longest=currentPos    
        #time to get all of the children of this node and add them to the queue
        room=self.getLocation(currentPos[0])
        for door in room.connectingRooms:
            queue.append([room.connectingRooms[door], currentPos[1]+1])
        visited.append(currentPos[0])
        return self.__longestPath(queue, visited, longest)
    def generateObstacles(self):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if isinstance(self.levelGrid[i][j],Room):
                    if (i,j)==self.bossRoom:
                        continue
                    self.__generateObstacles(self.levelGrid[i][j])
    def __generateObstacles(self, room, debug=False):
        locationList=[(2,2),(2,3),(2,4),(2,7),(2,11),(2,13),(2,14),(2,15),(2,16),
                      (3,2),(3,8),(3,10),(3,13),(3,14),(3,15),(3,15),(3,16),
                      (4,2),(4,5),(4,6),(4,8),(4,10),
                      (5,5),(5,6),(5,13),(5,14),(5,15),(5,16),
                      (6,3),(6,8),(6,9),(6,10),(6,13),(6,16),
                      (7,4),
                      (8,2),(8,6),(8,7),(8,10),(8,11),(8,15),(8,16),
                      (9,3),(9,8),(9,10),(9,14),(9,15),
                      (10,3),(10,4),(10,13),(10,14),
                      (11,4),(11,5),(11,13),(11,16),
                      (12,6)]
        if debug:
            #need 19 across and 15 down
            roomGrid=[['*']*19 for x in range(15)]
            for i in range(19):
                roomGrid[0][i]='~'
                roomGrid[14][i]='~'
            for i in range(15):
                roomGrid[i][0]='~'
                roomGrid[i][18]='~'
            #for i in range(len(locationList)):
            #    roomGrid[locationList[i][0]][locationList[i][1]]='X'
            #self.printRoom(roomGrid)
        #go through the list and determine if we are placing an object
        for i in range(len(locationList)):
            if bool(random.randint(0,1)):
                #place the object!
                if debug:
                    roomGrid[locationList[i][0]][locationList[i][1]]='X'
                x=32+(locationList[i][1]*32)
                y=(locationList[i][0]*32)
                obj=Obstacle((x,y),'rock.png')
                room.walls.add(obj)
                room.obstacles.add(obj)
        if debug:
            self.printRoom(roomGrid)


        
    def printRoom(self, roomGrid):
        for i in range(15):
            line=''
            for j in range(19):
                line+=roomGrid[i][j]
            print line
        print
    def printGrid(self):
        print "level: ",self.levelNumber
        for i in range(self.SIZE):
            line=''
            for j in range(self.SIZE):
                if self.levelGrid[j][i]==-1:
                    line+='.'
                elif (j,i)==self.rootRoom:
                    line+='!'
                elif (j,i)==self.bossRoom:
                    line+='B'
                else:
                    line+='*'
            print line
