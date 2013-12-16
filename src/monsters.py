'''
Created on Dec 15, 2013

@author: kristoffe
'''

import actor
import behaviors
import model
import pygame
from pygame import Rect
from pygame.locals import *
import random

MNM = {'name':'mnm', 'image':'mnm.png', 'behavior':behaviors.blue_mnm,
       'health':20, 'strength':2, 'is_boss':False, 'random_state':False,
       'init_state':['wait'], 'size': 32,
       'state_anims':{'wait':([Rect(0,0,32,32)], True, 1),
                      'move':([Rect(0,0,32,32), Rect(32,0,32,32),
                               Rect(0,0,32,32), Rect(64,0,32,32)],
                              True, 8),
                      'windup':([Rect(96,0,32,32)], True, 1),
                      'jump':([Rect(128,0,32,32)], True, 1)}
        }

class Monster(actor.Actor):
    
    def __init__(self, mon_type):
        if mon_type['random_state']:
            self.state = random.choice(mon_type['init_state'])
        else:
            self.state = mon_type['init_state'][0]
        self.prev_state = self.state
        actor.Actor.__init__(self, mon_type['image'],
                             Rect(0,0,mon_type['size'],mon_type['size']),
                             mon_type['state_anims'],
                             respawns = mon_type['is_boss'])
        self.name = mon_type['name']
        self.behavior = mon_type['behavior']
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.movepos = [0,0]
        self.hitcount = 0
        self.pushcount = 0
        self.cannot_collide = pygame.sprite.Group()
        self.health = mon_type['health']
        self.strength = mon_type['strength']
        self.waitcount = 0
        self.movecount = 0
        self.isBoss=mon_type['is_boss']
        random.seed()
        if self.state == 'wait':
            self.waitcount == random.randint(0,40)
    
    def getmovepos(self):
        return self.movepos
    
    def on_collision(self, sprite):
        if isinstance(sprite, model.Character):
            if (sprite.state == "move"):
                sprite.hitmove[0] = self.movepos[0]/3*8
                sprite.hitmove[1] = self.movepos[1]/3*8
                sprite.state = "hit"
            if (self.state != "hit"):
                self.movepos[0] = 0
                self.movepos[1] = 0
                self.state = "hit"
        if isinstance(sprite, model.Obstacle):
            if self.state == 'jump':
                self.state = 'wait'
                self.movepos = [0, 0]
        '''if isinstance(sprite, Monster):
            if (self.state == "hit" and sprite.state != "hit"):
                sprite.movepos[0] = self.movepos[0]
                sprite.movepos[1] = self.movepos[1]
                sprite.state = "hit"
                sprite.hitcount = self.hitcount''' 
        
    def update(self, obstacles, moveables, character):
        self.behavior(self, obstacles, moveables, character)
        actor.Actor.update(self, moveables, obstacles)