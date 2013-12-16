'''
Created on Dec 15, 2013

@author: kristoffe
'''

import pygame
import model
import random
import utils

def blue_mnm(object, obstacles, moveables, character):
    if object.state == "hit":
        if object.hitcount < 15:
            object.hitcount += 1
        else:
            object.hitcount = 0
            object.pushcount = 0
            object.waitcount = 0
            object.movecount = 0
            object.state = "wait"
            for current_collisions in pygame.sprite.spritecollide(object, moveables,0):
                object.cannot_collide.add(current_collisions)
        model.move(object, moveables, obstacles, object.movepos)
        pygame.event.pump()
        return
    
    if object.state != "hit" and object.state != "pushback" and object.state != "windup":
        if utils.distance(object.rect.topleft, character.rect.topleft) <= 96:
            object.target = character.rect.topleft
            object.state = "windup"
    
    if object.state == "windup":
        if object.waitcount < 20:
            object.waitcount += 1
        else:
            object.waitcount = 0
            vec = utils.convert_to_unit_vector(object.rect.x, character.rect.x, object.rect.y, character.rect.y)
            object.movepos = [vec[0] * 10, vec[1] * 10]
            object.state = "jump"
    
    if object.state == "jump":
        if object.rect.topleft == object.target:
            object.movepos = [0,0]
            object.state = "wait"
    
    if object.state == "pushback":
        if object.pushcount < 2:
            object.pushcount += 1
        else:
            object.pushcount = 0
            object.movepos = [0,0]
            object.state = "wait"
            
    if object.state == "wait":
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
            object.state = "wait"
    
    if abs(object.movepos[0]) < abs(object.movepos[1]):
        if object.movepos[1] < 0:
            object.dir = model.NORTH
        elif object.movepos[1] > 0:
            object.dir = model.SOUTH
    elif abs(object.movepos[0]) > abs(object.movepos[1]):
        if object.movepos[0] < 0:
            object.dir = model.WEST
        elif object.movepos[0] > 0:
            object.dir = model.EAST
    
    if object.state == "wait" or object.state == "move":
        
    
    model.move(object, moveables, obstacles, object.movepos)
    for current_collision in object.cannot_collide.sprites():
        if not current_collision in pygame.sprite.spritecollide(object, moveables, 0):
            object.cannot_collide.remove(current_collision)
    pygame.event.pump()

def green_mnm(object, obstacles, moveables, character):
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
                object.cannot_collide.add(current_collisions)
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
            myProjectile = model.Projectile('slimeball.png', 2)
            character.currentroom.projectiles.add(myProjectile)
            myProjectile.rect.center = object.rect.center
            vec = utils.convert_to_unit_vector(object.rect.x, character.rect.x, object.rect.y, character.rect.y)
            myProjectile.movepos = [int(vec[0] * 12), int(vec[1] * 12)]
            
            object.waitcount = 0
            object.state = "wait2"
            
    model.move(object, moveables, obstacles, object.movepos)
    for current_collision in object.cannot_collide.sprites():
        if not current_collision in pygame.sprite.spritecollide(object, moveables, 0):
            object.cannot_collide.remove(current_collision)
    pygame.event.pump()
