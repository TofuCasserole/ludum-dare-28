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
        self.health = 100
        #self.room = start_room
        state = "still"
        self.movepos = [0,0]
        self.tryingmoveright = False
        self.tryingmoveleft = False
        self.tryingmoveup = False
        self.tryingmovedown = False
        self.state = "move"
        self.hitcount = 0
        self.hitmove = [0,0]
        
    def update(self, obstacles):
        if self.state == "hit":
            if self.hitcount < 30:
                self.hitcount += 1
            else:
                self.state = "move"
                self.hitcount = 0
        
            newpos = self.rect.move([self.hitmove[0], 0])
            if self.area.contains(newpos):
                self.rect = newpos
                for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
                    if self.hitmove[0] > 0 and self.rect.right > obstacle.rect.left:
                        self.rect.right = obstacle.rect.left
                    if self.hitmove[0] < 0 and self.rect.left < obstacle.rect.right:
                        self.rect.left = obstacle.rect.right
            
            
            newpos = self.rect.move([0, self.hitmove[1]])
            if self.area.contains(newpos):
                self.rect = newpos
                for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
                    if self.hitmove[1] > 0 and self.rect.bottom > obstacle.rect.top:
                        self.rect.bottom = obstacle.rect.top
                    if self.hitmove[1] < 0 and self.rect.top < obstacle.rect.bottom:
                        self.rect.top = obstacle.rect.bottom
            pygame.event.pump()
            return
        
        newpos = self.rect.move([self.movepos[0], 0])
        if self.area.contains(newpos):
            self.rect = newpos
        for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
            if self.movepos[0] > 0 and self.rect.right > obstacle.rect.left:
                self.rect.right = obstacle.rect.left
            if self.movepos[0] < 0 and self.rect.left < obstacle.rect.right:
                self.rect.left = obstacle.rect.right
            
            
        newpos = self.rect.move([0, self.movepos[1]])
        if self.area.contains(newpos):
            self.rect = newpos
        for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
            if self.movepos[1] > 0 and self.rect.bottom > obstacle.rect.top:
                self.rect.bottom = obstacle.rect.top
            if self.movepos[1] < 0 and self.rect.top < obstacle.rect.bottom:
                self.rect.top = obstacle.rect.bottom
        pygame.event.pump()
        

class Monster(pygame.sprite.Sprite):
    def __init__(self, character, obstacles, monsters):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('wall.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        random.seed()
        self.rect.topleft = (random.randint(0,self.area.right-64), random.randint(0,self.area.bottom-64))
        while (pygame.sprite.spritecollide(self, character, 0) != [] or pygame.sprite.spritecollide(self, obstacles, 0) != []
               or pygame.sprite.spritecollide(self, monsters, 0) != []):
            self.rect.topleft = (random.randint(0,self.area.right), random.randint(0,self.area.bottom))
        self.state = "chase"
        self.movepos = [0,0]
        self.hitcount = 0
        
    def update(self, obstacles, monsters, character):
        if self.state == "hit":
            if self.hitcount < 30:
                self.hitcount += 1
            else:
                self.hitcount = 0
                self.state = "chase"
                
        if self.state == "chase":
            self.moveclock = 0
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
                
        newpos = self.rect.move([self.movepos[0], 0])
        if self.area.contains(newpos):
            self.rect = newpos
        for obstacle in pygame.sprite.spritecollide(self, obstacles, 0) + pygame.sprite.spritecollide(self, monsters, 0):
            if obstacle == self:
                continue
            if self.movepos[0] > 0 and self.rect.right > obstacle.rect.left:
                self.rect.right = obstacle.rect.left
            if self.movepos[0] < 0 and self.rect.left < obstacle.rect.right:
                self.rect.left = obstacle.rect.right
        if pygame.sprite.collide_rect(self, character) and self.state != "hit":
            character.state = "hit"
            character.hitmove[0] = self.movepos[0] 
            character.hitmove[1] = self.movepos[1]
            self.state = "hit"
            self.movepos[0] *=  -1
            self.movepos[1] *= -1
            
        newpos = self.rect.move([0, self.movepos[1]])
        if self.area.contains(newpos):
            self.rect = newpos
        for obstacle in pygame.sprite.spritecollide(self, obstacles, 0) + pygame.sprite.spritecollide(self, monsters, 0):
            if obstacle == self:
                continue
            if self.movepos[1] > 0 and self.rect.bottom > obstacle.rect.top:
                self.rect.bottom = obstacle.rect.top
            if self.movepos[1] < 0 and self.rect.top < obstacle.rect.bottom:
                self.rect.top = obstacle.rect.bottom
        if pygame.sprite.collide_rect(self, character) and self.state != "hit":
            character.state = "hit"
            character.hitmove[0] = self.movepos[0]
            character.hitmove[1] = self.movepos[1]
            self.state = "hit"
            self.movepos[0] *=  -1
            self.movepos[1] *= -1
        pygame.event.pump()
            

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('rock.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = location
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



class Room:
    def __init__(self, doors, obstacles=[], monsters=[]):
        self.doors = doors
        self.obstacles = obstacles
        self.monsters = monsters
        possible_locations = [(x,y) for x in range(0, WIDTH) for y in range (0, LENGTH) if (x,y) not in self.obstacles]
        random.shuffle(possible_locations)
        for monster in self.monsters:
            monster.location = possible_locations.pop()
            
    def monster_locations(self):
        return [monster.location for monster in self.monsters]
    
rooms = [[Room(WEST), Room(EAST)]]
cur_room_row = 0
cur_room_col = 0