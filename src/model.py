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
            image = pygame.transform.scale(image.convert(), (64, 64))
        else:
            image = pygame.transform.scale(image.convert_alpha(), (64, 64))
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
        
    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
        

class Monster(pygame.sprite.Sprite):
    def __init__(self, type):
        self.type = type
        self.location = False


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