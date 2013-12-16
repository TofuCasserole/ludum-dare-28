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
                object.cannot_collide.add(current_collisions)
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
            x_distance = abs(object.rect.x - character.rect.x)
            y_distance = abs(object.rect.y - character.rect.y)
            x_speed = 12*x_distance/(x_distance+y_distance)
            y_speed = 12*y_distance/(x_distance+y_distance)
            if object.rect.x > character.rect.x:
                x_speed *= -1
            if object.rect.y > character.rect.y:
                y_speed *= -1
            myProjectile.movepos = [x_speed, y_speed]
            
            
            object.waitcount = 0
            object.state = "wait2"
            
    model.move(object, moveables, obstacles, object.movepos)
    for current_collision in object.cannot_collide.sprites():
        if not current_collision in pygame.sprite.spritecollide(object, moveables, 0):
            object.cannot_collide.remove(current_collision)
    pygame.event.pump()

def Boss(object, obstacles, moveables, character):
    #states that can be chosen at random, move should not be a part of this
    states=['wait', 'charge', 'wander','walk_to_center']
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
    if object.state == "pushback":
        if object.pushcount < 2:
            object.pushcount += 1
        else:
            object.pushcount = 0
            object.movepos = [0,0]
            object.state = "wait"
    #wait state 
    if object.state == "wait":
        if object.waitcount < 40:
            object.waitcount += 1
        else:
            object.waitcount = 0
            object.state = random.choice(states)
            if object.state=='wander':                
                object.movepos[0] = random.randint(-1,1)*3
                object.movepos[1] = random.randint(-1,1)*3
                object.state='wait'

    #640x480 offset by 32
    if object.state=='walk_to_center':
        if object.waitcount < 40:
            object.waitcount += 1
        else:
            x_distance = abs(object.rect.x - ((640/2)+32))
            y_distance = abs(object.rect.y - (480/2))
            x_speed = 12*x_distance/(x_distance+y_distance)
            y_speed = 12*y_distance/(x_distance+y_distance)
            if object.rect.x > ((640/2)+32):
                x_speed *= -1
            if object.rect.y > (480/2):
                y_speed *= -1
            object.movepos = [x_speed, y_speed]
            object.waitcount=0
            object.state='wait'
    if object.state=='charge':
        if object.waitcount < 40:
            object.waitcount+=1
        else:
            x_distance = abs(object.rect.x - character.rect.x)
            y_distance = abs(object.rect.y - character.rect.y)
            x_speed = 20*x_distance/(x_distance+y_distance)
            y_speed = 20*y_distance/(x_distance+y_distance)
            if object.rect.x > character.rect.x:
                x_speed *= -1
            if object.rect.y > character.rect.y:
                y_speed *= -1
            object.movepos = [x_speed, y_speed] 
            object.waitcount = 0
            object.state = "wait"

    model.move(object, moveables, obstacles, object.movepos)
    for current_collision in object.cannot_collide.sprites():
        if not current_collision in pygame.sprite.spritecollide(object, moveables, 0):
            object.cannot_collide.remove(current_collision)
    pygame.event.pump()
