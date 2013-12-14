'''
Created on Dec 13, 2013

@author: thedoctor
'''
DALEK = 0
CYBERMAN = 1
WEEPINGANGELS = 2
SILENCE = 3

EAST = "east"
WEST = "west"
NORTH = "north"
SOUTH = "south"

LENGTH = 9
WIDTH = 13

import os
import random
import pygame
from pygame.locals import *

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('../', 'res', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = pygame.transform.scale(image.convert(), (32, 32))
        else:
            image = pygame.transform.scale(image.convert_alpha(), (32, 32))
    except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
    return image, image.get_rect()

class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('char.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.midleft = self.area.midleft
        self.rect = self.rect.move((64,0))
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
    
    def getmovepos(self):
        if self.state == "hit":
            return self.hitmove
        else:
            return self.movepos
        
    def on_collision(self, sprite):
        pass
            
    def update(self, obstacles, moveables):
        self.sword_cooldown += 1
        
        if self.state == "hit":
            if self.hitcount < 15:
                self.hitcount += 1
            else:
                self.state = "invulnerable"
                self.hitcount = 0
        
        if self.state == "invulnerable":
            if self.invuln_count < 10:
                self.invuln_count += 1
            else:
                self.invuln_count = 0
                self.state = "move"
                
        move(self, moveables, obstacles, self.getmovepos())
        pygame.event.pump()
        

class Monster(pygame.sprite.Sprite):
    def __init__(self, character, obstacles, monsters):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('slime.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        random.seed()
        self.rect.topleft = (random.randint(0,self.area.right-32), random.randint(0,self.area.bottom-32))
        while (pygame.sprite.spritecollide(self, character, 0) != [] or pygame.sprite.spritecollide(self, obstacles, 0) != []
               or pygame.sprite.spritecollide(self, monsters, 0) != []):
            self.rect.topleft = (random.randint(0,self.area.right), random.randint(0,self.area.bottom))
        self.state = "chase"
        self.movepos = [0,0]
        self.hitcount = 0
        self.pushcount = 0
        
    def getmovepos(self):
        return self.movepos
    
    def on_collision(self, sprite):
        if isinstance(sprite, Character):
            if (sprite.state == "move"):
                sprite.hitmove[0] = self.movepos[0]/2
                sprite.hitmove[1] = self.movepos[1]/2
                sprite.state = "hit"
            if (self.state != "hit"):
                self.movepos[0] = 0
                self.movepos[1] = 0
                self.state = "hit"
        '''if isinstance(sprite, Monster):
            if (self.state == "hit" and sprite.state != "hit"):
                sprite.movepos[0] = self.movepos[0]
                sprite.movepos[1] = self.movepos[1]
                sprite.state = "hit"
                sprite.hitcount = self.hitcount'''   
            
        
    def update(self, obstacles, moveables, character):
        if self.state == "hit":
            if self.hitcount < 15:
                self.hitcount += 1
            else:
                self.hitcount = 0
                self.state = "chase"
        
        if self.state == "pushback":
            if self.pushcount < 2:
                self.pushcount += 1
            else:
                self.pushcount = 0
                self.state = "chase"
                
        if self.state == "chase":
            if self.rect.top > character.rect.top:
                self.movepos[1] = -2
            elif self.rect.bottom < character.rect.bottom:
                self.movepos[1] = 2
            else:
                self.movepos[1] = 0
            if self.rect.left > character.rect.left:
                self.movepos[0] = -2
            elif self.rect.right < character.rect.right:
                self.movepos[0] = 2
            else:
                self.movepos[0] = 0
                
        move(self, moveables, obstacles, self.movepos)
    
        pygame.event.pump()

class Sword(pygame.sprite.Sprite):
    def __init__(self, character):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('sword.png')
        self.rotate = 90
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
        if self.count > 20:
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
            if character.last_direction_moved == "right":
                monster.movepos = [16, 0]
            elif character.last_direction_moved == "left":
                monster.movepos = [-16, 0]
            elif character.last_direction_moved == "down":
                monster.movepos = [0, 16]
            elif character.last_direction_moved == "up":
                monster.movepos = [0, -16]
        self.count += 1

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, location, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(sprite)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
    
        self.rect.topleft = location

class Door(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.rect.x = xpos
        self.rect.y = ypos
        self.rect.w = 32
        self.rect.h = 32
        
    def update(self, character):
        if pygame.sprite.collide_mask(self, character):
            print("Door registered!")
        
'''
doors are passed as an array of "east", "north", "south", and "west"

obstacles are passed as a list array of 2 tuples with the y parameter first and the x
parameter second, starting at 0,0 in the top left corner e.g.,
-------------------
| 0,0 | 0,1 | 0,2 |
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
    if sprite.area.contains(newpos) and not realign:
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
            sprite.rect.right = moveable.rect.left
            sprite.on_collision(moveable)
            moveable.on_collision(sprite)
            for moveable2 in pygame.sprite.spritecollide(sprite, moveables, 0):
                if moveable2 == sprite:
                    continue
                move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
        if movepos[0] < 0 and sprite.rect.left < moveable.rect.right:
            sprite.rect.left = moveable.rect.right
            sprite.on_collision(moveable)
            moveable.on_collision(sprite)
            for moveable2 in pygame.sprite.spritecollide(sprite, moveables, 0):
                if moveable2 == sprite:
                    continue
                move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
    newpos = sprite.rect.move([0, movepos[1]])
    if sprite.area.contains(newpos) and not realign:
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
            sprite.rect.bottom = moveable.rect.top
            sprite.on_collision(moveable)
            moveable.on_collision(sprite)
            for moveable2 in pygame.sprite.spritecollide(sprite, moveables, 0):
                if moveable2 == sprite:
                    continue
                move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
        if movepos[1] < 0 and sprite.rect.top < moveable.rect.bottom:
            sprite.rect.top = moveable.rect.bottom
            sprite.on_collision(moveable)
            moveable.on_collision(sprite)
            for moveable2 in pygame.sprite.spritecollide(sprite, moveables, 0):
                if moveable2 == sprite:
                    continue
                move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
    
        
    
        
        

class Room:
    def __init__(self, doors, obstacles=None, monsters=None):
        self.doors = doors
        self.obstacles = obstacles
        self.monsters = monsters
        possible_locations = [(x,y) for x in range(0, WIDTH) for y in range (0, LENGTH) if (x,y) not in self.obstacles]
        random.shuffle(possible_locations)
        for monster in self.monsters:
            monster.location = possible_locations.pop()
        self.walls = pygame.sprite.RenderPlain()
        # generate north/south walls
        for x in range(32, 640, 32):
            if not (x == 320 and NORTH in doors):
                self.walls.add(Obstacle((x, 0), "wall.png"))
            if not (x == 320 and SOUTH in doors):
                self.walls.add(Obstacle((x, 448), "wall.png"))
        # generate east/west walls
        for y in range(0, 480, 32):
            if not (y == 224 and WEST in doors):
                self.walls.add(Obstacle((32, y), "wall.png"))
            if not (y == 224 and EAST in doors):
                self.walls.add(Obstacle((608, y), "wall.png"))    
    
    def monster_locations(self):
        return [monster.location for monster in self.monsters]

cur_room_row = 0
cur_room_col = 0
