'''
Created on Dec 14, 2013

@author: kristoffe
'''
import pygame
import os
import model
from spritesheet import SpriteSheet

class HealthBar():
    
    def __init__(self):
        self.sheet = SpriteSheet(model.load_png("gui.png"))
        self.value = 100
    
    def draw(self, surface):
        surface.blit(self.sheet.image_at((32,0,64,16)), (0,0))