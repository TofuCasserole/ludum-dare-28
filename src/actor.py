'''
Created on Dec 15, 2013

@author: kristoffe
'''

import pygame
import spritesheet
import model

class Actor(pygame.sprite.Sprite):
    
    def __init__(self, image, rect):
        self.sheet = spritesheet.SpriteSheet(pygame.transform.scale2x(model.load_png(image)))
        self.rect = rect
        
    
    def update(self, action):
        pass