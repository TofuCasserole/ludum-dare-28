'''
Created on Dec 15, 2013

@author: kristoffe
'''

import pygame
import model

def blue_mnm(object, obstacles, moveables, character):
    if object.state == "hit":
            if object.hitcount < 15:
                object.hitcount += 1
            else:
                object.hitcount = 0
                object.state = "chase"
    
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
    pygame.event.pump()