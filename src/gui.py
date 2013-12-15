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
        self.sheet = SpriteSheet(pygame.transform.scale2x(model.load_png("gui.png")))
        self.health = 100
    
    def draw(self, surface):
        surface.blit(self.sheet.image_at((32,0,64,16)), (0,0))
        surface.blit(self.sheet.image_at((64,0,96,1)), (0,18))
        for bar_lvl in range(1,41):
            y_val = bar_lvl + 18
            if (bar_lvl % 4) == 0 and bar_lvl != 40:
                surface.blit(self.sheet.image_at((64,2,96,3)), (0, y_val))
            else:
                surface.blit(self.sheet.image_at((64,1,96,2)), (0, y_val))
            if self.health >= (40 - bar_lvl) * 2.5:
                surface.blit(self.sheet.image_at((64,3,96,4)), (0, y_val))
            else:
                surface.blit(self.sheet.image_at((64,4,96,5)), (0, y_val))
