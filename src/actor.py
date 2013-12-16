'''
Created on Dec 15, 2013

@author: kristoffe
'''

import pygame
import spritesheet
import model

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

class Actor(pygame.sprite.Sprite):
    
    def __init__(self, image, rect):
        self.sheet = spritesheet.SpriteSheet(pygame.transform.scale2x(model.load_png(image)))
        self.movepos = [0,0]
        self.rect = rect
        
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
    
    def update(self, action, moveables, obstacles):
        action(self, moveables, obstacles)

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
            self.rect.center = self.area.center
        pygame.event.pump()