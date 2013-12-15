'''
Created on Dec 15, 2013

@author: kristoffe
'''

import pygame
import model
import random

def blue_mnm(object, obstacles, moveables, character):
    if object.state == "hit":
        if object.hitcount < 15:
            object.hitcount += 1
        else:
            object.hitcount = 0
            object.state = "chase"
            for current_collisions in pygame.sprite.spritecollide(object, moveables,0):
                object.can_collide.add(current_collisions)
        model.move(object, moveables, obstacles, object.movepos)
        pygame.event.pump()
        return
            
    if object.state == "pushback":
        if object.pushcount < 2:
            object.pushcount += 1
        else:
            object.pushcount = 0
            object.state = "chase"
    
    if object.state == "chase":
        if object.rect.top > character.rect.top:
            object.movepos[1] = -3
        elif object.rect.bottom < character.rect.bottom:
            object.movepos[1] = 3
        else:
            object.movepos[1] = 0
        if object.rect.left > character.rect.left:
            object.movepos[0] = -3
        elif object.rect.right < character.rect.right:
            object.movepos[0] = 3
        else:
            object.movepos[0] = 0
    
    
    model.move(object, moveables, obstacles, object.movepos)
    for current_collision in object.can_collide.sprites():
        if not current_collision in pygame.sprite.spritecollide(object, moveables, 0):
            object.can_collide.remove(current_collision)
    pygame.event.pump()

def green_mnm(object, obstacles, moveables, characters):
    if object.state == "hit":
        if object.hitcount < 15:
            object.hitcount += 1
        else:
            object.hitcount = 0
            object.pushcount = 0
            object.waitcount = 0
            object.movecount = 0
            object.state = "wait2"
            for current_collisions in pygame.sprite.spritecollide(object, moveables,0):
                object.can_collide.add(current_collisions)
        model.move(object, moveables, obstacles, object.movepos)
        pygame.event.pump()
        return
   
    if object.state == "pushback":
        if object.pushcount < 2:
            object.pushcount += 1
        else:
            object.pushcount = 0
            object.movepos = [0,0]
            object.state = "wait2"
            
    if object.state == "wait2":
        if object.waitcount < 40:
            object.waitcount += 1
        else:
            random.seed()
            object.waitcount = 0
            object.movepos[0] = random.randint(-1,1)*3
            object.movepos[1] = random.randint(-1,1)*3
            object.state = "move"
            
    if object.state == "move":
        if object.movecount < 60:
            object.movecount += 1
        else:
            object.movecount = 0
            object.movepos = [0,0]
            object.state = "wait1"
            
    if object.state == "wait1":
        if object.waitcount < 40:
            object.waitcount += 1
        else:
            myProjectile = model.Projectile()
            object.waitcount = 0
            object.state = "wait2"