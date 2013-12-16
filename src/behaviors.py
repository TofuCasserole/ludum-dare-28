'''
Created on Dec 15, 2013

@author: kristoffe
'''

import pygame
import model
import random
import utils

def blue_mnm(sprite, obstacles, moveables, character):
    if sprite.state == "hit":
        if sprite.hitcount < 15:
            sprite.hitcount += 1
        else:
            sprite.hitcount = 0
            sprite.pushcount = 0
            sprite.waitcount = 0
            sprite.movecount = 0
            sprite.state = "wait"
            for current_collisions in pygame.sprite.spritecollide(sprite, moveables,0):
                sprite.cannot_collide.add(current_collisions)
        return
    
    if sprite.state != "hit" and sprite.state != "pushback" and sprite.state != "windup" and sprite.state != "jump":
        if utils.distance(sprite.rect.center, character.rect.center) <= 100:
            sprite.target = character.rect.center
            sprite.waitcount = 0
            sprite.movecount = 0
            sprite.movepos = [0,0]
            sprite.state = "windup"
    
    if sprite.state == "windup":
        if sprite.waitcount < 20:
            sprite.waitcount += 1
        else:
            sprite.waitcount = 0
            vec = utils.convert_to_unit_vector(sprite.rect.x, character.rect.x, sprite.rect.y, character.rect.y)
            sprite.movepos = [vec[0] * 10, vec[1] * 10]
            sprite.state = "jump"
    
    if sprite.state == "jump":
        if ((sprite.movepos[0] >= 0 and sprite.movepos[1] >= 0 and sprite.rect.x >= sprite.target[0] and sprite.rect.y >= sprite.target[1]) or
            (sprite.movepos[0] >= 0 and sprite.movepos[1] <= 0 and sprite.rect.x >= sprite.target[0] and sprite.rect.y <= sprite.target[1]) or
            (sprite.movepos[0] <= 0 and sprite.movepos[1] <= 0 and sprite.rect.x <= sprite.target[0] and sprite.rect.y >= sprite.target[1]) or
            (sprite.movepos[0] <= 0 and sprite.movepos[1] <= 0 and sprite.rect.x <= sprite.target[0] and sprite.rect.y <= sprite.target[1]) or
            pygame.sprite.spritecollide(sprite, obstacles, 0) != []):
            sprite.movepos = [0,0]
            sprite.state = "wait"
    
    if sprite.state == "pushback":
        if sprite.pushcount < 2:
            sprite.pushcount += 1
        else:
            sprite.pushcount = 0
            sprite.movepos = [0,0]
            sprite.state = "wait"
            
    if sprite.state == "wait":
        if sprite.waitcount < 40:
            sprite.waitcount += 1
        else:
            random.seed()
            sprite.waitcount = 0
            sprite.movepos[0] = random.randint(-1,1)*3
            sprite.movepos[1] = random.randint(-1,1)*3
            sprite.state = "move"
            
    if sprite.state == "move":
        if sprite.movecount < 60:
            sprite.movecount += 1
        else:
            sprite.movecount = 0
            sprite.movepos = [0,0]
            sprite.state = "wait"

def green_mnm(sprite, obstacles, moveables, character):
    if sprite.state == "hit":
        if sprite.hitcount < 15:
            sprite.hitcount += 1
        else:
            sprite.hitcount = 0
            sprite.pushcount = 0
            sprite.waitcount = 0
            sprite.movecount = 0
            sprite.state = "wait2"
            for current_collisions in pygame.sprite.spritecollide(sprite, moveables,0):
                sprite.cannot_collide.add(current_collisions)
        return
   
    if sprite.state == "pushback":
        if sprite.pushcount < 2:
            sprite.pushcount += 1
        else:
            sprite.pushcount = 0
            sprite.movepos = [0,0]
            sprite.state = "wait2"
            
    if sprite.state == "wait2":
        if sprite.waitcount < 40:
            sprite.waitcount += 1
        else:
            random.seed()
            sprite.waitcount = 0
            sprite.movepos[0] = random.randint(-1,1)*3
            sprite.movepos[1] = random.randint(-1,1)*3
            sprite.state = "move"
            
    if sprite.state == "move":
        if sprite.movecount < 60:
            sprite.movecount += 1
        else:
            sprite.movecount = 0
            sprite.movepos = [0,0]
            sprite.state = "wait1"
            
    if sprite.state == "wait1":
        if sprite.waitcount < 40:
            sprite.waitcount += 1
        else:
            myProjectile = model.Projectile('slimeball.png', 2)
            character.currentroom.projectiles.add(myProjectile)
            myProjectile.rect.center = sprite.rect.center
            vec = utils.convert_to_unit_vector(sprite.rect.x, character.rect.x, sprite.rect.y, character.rect.y)
            myProjectile.movepos = [int(vec[0] * 12), int(vec[1] * 12)]
            sprite.state = 'wait2'
            sprite.waitcount = 0

def Boss(sprite, obstacles, moveables, character):
    #states that can be chosen at random, move should not be a part of this
    states=['wait', 'charge', 'wander','walk_to_center']
    if sprite.state == "hit":
        if sprite.hitcount < 15:
            sprite.hitcount += 1
        else:
            sprite.hitcount = 0
            sprite.pushcount = 0
            sprite.waitcount = 0
            sprite.movecount = 0
            sprite.state = "wait"
            for current_collisions in pygame.sprite.spritecollide(sprite, moveables,0):
                sprite.cannot_collide.add(current_collisions)
        return
    if sprite.state == "pushback":
        if sprite.pushcount < 2:
            sprite.pushcount += 1
        else:
            sprite.pushcount = 0
            sprite.movepos = [0,0]
            sprite.state = "wait"
    #wait state 
    if sprite.state == "wait":
        if sprite.waitcount < 40:
            sprite.waitcount += 1
        else:
            sprite.waitcount = 0
            sprite.state = random.choice(states)
            if sprite.state=='wander':                
                sprite.movepos[0] = random.randint(-1,1)*3
                sprite.movepos[1] = random.randint(-1,1)*3
                sprite.state='wait'

    #640x480 offset by 32
    if sprite.state=='walk_to_center':
        if sprite.waitcount < 40:
            sprite.waitcount += 1
        else:
            x_distance = abs(sprite.rect.x - ((640/2)+32))
            y_distance = abs(sprite.rect.y - (480/2))
            x_speed = 12*x_distance/(x_distance+y_distance)
            y_speed = 12*y_distance/(x_distance+y_distance)
            if sprite.rect.x > ((640/2)+32):
                x_speed *= -1
            if sprite.rect.y > (480/2):
                y_speed *= -1
            sprite.movepos = [x_speed, y_speed]
            sprite.waitcount=0
            sprite.state='wait'
    if sprite.state=='charge':
        if sprite.waitcount < 40:
            sprite.waitcount+=1
        else:
            x_distance = abs(sprite.rect.x - character.rect.x)
            y_distance = abs(sprite.rect.y - character.rect.y)
            x_speed = 20*x_distance/(x_distance+y_distance)
            y_speed = 20*y_distance/(x_distance+y_distance)
            if sprite.rect.x > character.rect.x:
                x_speed *= -1
            if sprite.rect.y > character.rect.y:
                y_speed *= -1
            sprite.movepos = [x_speed, y_speed] 
            sprite.waitcount = 0
            sprite.state = "wait"
