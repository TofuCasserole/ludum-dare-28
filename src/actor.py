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

def create_anim(state_name, arguments, sheet):
    return (state_name, spritesheet.SpriteStripAnim(sheet, *arguments))

class Actor(pygame.sprite.Sprite):
    
    def __init__(self, image, rectangle, state_anims, animated=True, respawns=False):
        pygame.sprite.Sprite.__init__(self)
        self.respawns = respawns
        self.isdirectional = animated
        temp_rect = image.get_rect()
        if animated:
            self.dir = DOWN
            sheet = spritesheet.SpriteSheet(image)
            upsheet = sheet.subsheet(Rect(0,0,temp_rect.w,rectangle.h))
            downsheet = sheet.subsheet(Rect(0,32,temp_rect.w,rectangle.h))
            leftsheet = sheet.subsheet(Rect(0,96,temp_rect.w,rectangle.h))
            rightsheet = sheet.subsheet(Rect(0,64,temp_rect.w,rectangle.h))
            self.upanims = dict(map(lambda (k,v): create_anim(k,v,upsheet), state_anims.iteritems()))
            self.downanims = dict(map(lambda (k,v): create_anim(k,v,downsheet), state_anims.iteritems()))
            self.leftanims = dict(map(lambda (k,v): create_anim(k,v,leftsheet), state_anims.iteritems()))
            self.rightanims = dict(map(lambda (k,v): create_anim(k,v,rightsheet), state_anims.iteritems()))
            self.default_img = sheet.image_at(rectangle)
            self.current_anim = self.downanims.get(self.state).iter()
            self.image = self.default_img
        else:
            self.image = image
        self.rect = rectangle
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
                    Actor.move(moveable, moveables, obstacles, moveable.getmovepos(), True)
            if movepos[0] < 0 and self.rect.left < obstacle.rect.right:
                self.rect.left = obstacle.rect.right
                for moveable in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable == self:
                        continue
                    Actor.move(moveable, moveables, obstacles, moveable.getmovepos(), True)
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
                    Actor.move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
            if movepos[0] < 0 and self.rect.left < moveable.rect.right:
                if not self.cannot_collide.has(moveable) and not moveable.cannot_collide.has(self):
                    self.rect.left = moveable.rect.right
                self.on_collision(moveable)
                moveable.on_collision(self)
                for moveable2 in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable2 == self:
                        continue
                    Actor.move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
        newpos = self.rect.move([0, movepos[1]])
        if not realign:
            self.rect = newpos
        for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
            if movepos[1] > 0 and self.rect.bottom > obstacle.rect.top:
                self.rect.bottom = obstacle.rect.top
                for moveable in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable == self:
                        continue
                    Actor.move(moveable, moveables, obstacles, moveable.getmovepos(), True)
            if movepos[1] < 0 and self.rect.top < obstacle.rect.bottom:
                self.rect.top = obstacle.rect.bottom
                for moveable in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable == self:
                        continue
                    Actor.move(moveable, moveables, obstacles, moveable.getmovepos(), True)
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
                    Actor.move(moveable2, moveables, obstacles, moveable2.getmovepos(), True)
            if movepos[1] < 0 and self.rect.top < moveable.rect.bottom:
                if not self.cannot_collide.has(moveable) and not moveable.cannot_collide.has(self):
                    self.rect.top = moveable.rect.bottom
                self.on_collision(moveable)
                moveable.on_collision(self)
                for moveable2 in pygame.sprite.spritecollide(self, moveables, 0):
                    if moveable2 == self:
                        continue
                    Actor.move(moveable, moveables, obstacles, moveable2.getmovepos(), True)
    
    def update(self, moveables, obstacles):
        if self.isdirectional:
            anim = self.downanims
            if abs(self.movepos[0]) < abs(self.movepos[1]):
                if self.movepos[1] < 0:
                    anim = self.upanims
                elif self.movepos[1] >= 0:
                    anim = self.downanims
            elif abs(self.movepos[0]) > abs(self.movepos[1]):
                if self.movepos[0] < 0:
                    anim = self.leftanims
                elif self.movepos[0] > 0:
                    anim = self.rightanims
        
            if self.state in anim.keys():
                if self.prev_state != self.state:
                    self.current_anim = anim.get(self.state).iter()
                    self.prev_state = self.state
                self.image = self.current_anim.next()
            else:
                self.image = self.default_img
        
        self.move(moveables, obstacles, self.getmovepos())
        for current_collision in self.cannot_collide.sprites():
            if not current_collision in pygame.sprite.spritecollide(self, moveables, 0):
                self.cannot_collide.remove(current_collision)
        if self.rect.right < 32 or self.rect.left > 608 or self.rect.bottom < 32 or self.rect.top > 448:
            if self.respawns:
                self.rect.center = self.area.center
        pygame.event.pump()