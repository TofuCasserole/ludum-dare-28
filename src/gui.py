'''
Created on Dec 14, 2013

@author: kristoffe
'''
import pygame
import utils
from spritesheet import SpriteSheet

class HealthBar():
    
    def __init__(self):
        self.sheet = SpriteSheet(pygame.transform.scale2x(utils.load_png("gui.png")))
        self.health = 100
    
    def draw(self, surface):
        surface.blit(self.sheet.image_at((32,0,32,16)), (0,0))
        surface.blit(self.sheet.image_at((64,0,32,2)), (0,18))
        for bar_lvl in range(1,81,2):
            y_val = bar_lvl + 19
            if self.health >= (40 - bar_lvl/2) * 2.5:
                surface.blit(self.sheet.image_at((64,2,32,2)), (0, y_val))
            else:
                surface.blit(self.sheet.image_at((64,4,32,2)), (0, y_val))
        surface.blit(self.sheet.image_at((64,0,32,2)), (0,100))