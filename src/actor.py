'''
Created on Dec 15, 2013

@author: kristoffe
'''

import pygame
from pygame import Rect
import spritesheet
import utils

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def create_anim(state_name, rectangles, sheet):
    return (state_name, spritesheet.SpriteStripAnim(sheet, rectangles))

class Actor(pygame.sprite.Sprite):
    
    def __init__(self, image, rectangle, state_anims, directional=True, respawns=False):
        self.respawns = respawns
        self.isdirectional = directional
        img = pygame.transform.scale2x(utils.load_png(image))
        if directional:
            sheet = spritesheet.SpriteSheet(img)
            upsheet = sheet.subsheet(Rect(0,0,img.rect.w,rectangle.h))
            downsheet = sheet.subsheet(Rect(0,32,img.rect.w,rectangle.h))
            leftsheet = sheet.subsheet(Rect(0,64,img.rect.w,rectangle.h))
            rightsheet = sheet.subsheet(Rect(0,96,img.rect.w,rectangle.h))
            upanims = dict(map(lambda (k,v):))
            self.rect = rectangle
        else:
            self.image = img
            self.rect = img.rect
        self.movepos = [0,0]
        
    def move(self, moveables, obstacles, movepos, realign = False):
        newpos = self.rect.move([movepos[0], 0])
        if not realign:
            self.rect = newpos
        for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
            if movepos[0] > 0 and self.rect.right > obstacle.rect.left:
                self.rect.right = obstacle.rect.left
                for moveable in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable == self:
                        continue
                    self.move(moveable, moveables, obstacles, moveable.getmovepos(), True)
            if movepos[0] < 0 and self.rect.left < obstacle.rect.right:
                self.rect.left = obstacle.rect.right
                for moveable in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable == self:
                        continue
                    self.move(moveable, moveables, obstacles, moveable.getmovepos(), True)
        for moveable in pygame.sprite.spritecollide(self, moveables, 0):
            if moveable == self:
                continue
            if movepos[0] > 0 and self.rect.right > moveable.rect.left:
                if not self.cannot_collide.has(moveable) and not moveable.cannot_collide.has(self):
                    self.rect.right = moveable.rect.left
                self.on_collision(moveable)
                moveable.on_collision(self)
                for moveable2 in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable2 == self:
                        continue
                    self.move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
            if movepos[0] < 0 and self.rect.left < moveable.rect.right:
                if not self.cannot_collide.has(moveable) and not moveable.cannot_collide.has(self):
                    self.rect.left = moveable.rect.right
                self.on_collision(moveable)
                moveable.on_collision(self)
                for moveable2 in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable2 == self:
                        continue
                    self.move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
        newpos = self.rect.move([0, movepos[1]])
        if not realign:
            self.rect = newpos
        for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
            if movepos[1] > 0 and self.rect.bottom > obstacle.rect.top:
                self.rect.bottom = obstacle.rect.top
                for moveable in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable == self:
                        continue
                    self.move(moveable, moveables, obstacles, moveable.getmovepos(), True)
            if movepos[1] < 0 and self.rect.top < obstacle.rect.bottom:
                self.rect.top = obstacle.rect.bottom
                for moveable in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable == self:
                        continue
                    self.move(moveable, moveables, obstacles, moveable.getmovepos(), True)
        for moveable in pygame.sprite.spritecollide(self, moveables, 0):
            if moveable == self:
                continue
            if movepos[1] > 0 and self.rect.bottom > moveable.rect.top:
                if not self.cannot_collide.has(moveable) and not moveable.cannot_collide.has(self):
                    self.rect.bottom = moveable.rect.top
                self.on_collision(moveable)
                moveable.on_collision(self)
                for moveable2 in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable2 == self:
                        continue
                    self.move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
            if movepos[1] < 0 and self.rect.top < moveable.rect.bottom:
                if not self.cannot_collide.has(moveable) and not moveable.cannot_collide.has(self):
                    self.rect.top = moveable.rect.bottom
                self.on_collision(moveable)
                moveable.on_collision(self)
                for moveable2 in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable2 == self:
                        continue
                    self.move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
    
    def update(self, moveables, obstacles):
        if self.isdirectional:
            if abs(self.movepos[0]) < abs(self.movepos[1]):
                if self.movepos[1] < 0:
                    self.dir = UP
                elif self.movepos[1] > 0:
                    self.dir = DOWN
            elif abs(self.movepos[0]) > abs(self.movepos[1]):
                if self.movepos[0] < 0:
                    self.dir = LEFT
                elif self.movepos[0] > 0:
                    self.dir = RIGHT
        
        self.move(moveables, obstacles, self.getmovepos())
        for current_collision in self.cannot_collide.sprites():
            if not current_collision in pygame.sprite.spritecollide(self, moveables, 0):
                self.cannot_collide.remove(current_collision)
        if self.rect.right < 32 or self.rect.left > 608 or self.rect.bottom < 32 or self.rect.top > 448:
            if self.respawns:
                self.rect.center = self.area.center
        pygame.event.pump()