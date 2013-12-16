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
    
    def draw(self, surface, level):
        surface.blit(self.sheet.image_at((32,0,32,16)), (0,0))
        surface.blit(self.sheet.image_at((64,0,32,2)), (0,18))
        for bar_lvl in range(1,81,2):
            y_val = bar_lvl + 19
            if self.health >= (40 - bar_lvl/2) * 2.5:
                surface.blit(self.sheet.image_at((64,2,32,2)), (0, y_val))
            else:
                surface.blit(self.sheet.image_at((64,4,32,2)), (0, y_val))
        surface.blit(self.sheet.image_at((64,0,32,2)), (0,100))
        utils.text_format(surface, 'LVL', 12, (0,129), (255,255,255), 3)
        if level.levelNumber < 10:
            utils.text_format(surface, str(level.levelNumber), 18, (8, 145), (255,255,255), 1)
        elif level.levelNumber < 100:
            utils.text_format(surface, str(level.levelNumber), 18, (2, 145), (255,255,255), 2)
        else:
            utils.text_format(surface, str(level.levelNumber), 13, (0, 145), (255,255,255), 3)
        utils.text_format(surface, "MSTR LEFT", 9, (0,223),(255,255,255), 4)
        if level.num_monsters > 9:
            utils.text_format(surface, str(level.num_monsters), 18, (2,255), (255,255,255), 2)
        else:
            utils.text_format(surface, str(level.num_monsters), 18, (8,255), (255,255,255), 1)
        utils.text_format(surface, "RGN", 12, (0,333), (255,255,255), 3)
        if level.health > 9:
            utils.text_format(surface, str(int(level.health)), 18, (2,349), (255,255,255), 2)
        else:
            utils.text_format(surface, str(int(level.health)), 18, (8,349), (255,255,255), 1)