'''
Created on Dec 13, 2013

@author: kristoffe
'''
import pygame
from pygame.locals import *
import model

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
        
    global character
    character = model.Character()
    
    clock = pygame.time.Clock()
    
    charactersprites = pygame.sprite.RenderUpdates(character)
    
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    while True:
        clock.tick(60)
        event_list = [event for event in pygame.event.get()]
        for event in event_list:
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_a:
                    cont = False
                    for event2 in event_list:
                        if event2.type == KEYDOWN and event2.key == K_d:
                            cont = True
                    if cont: continue
                    character.movepos[0] = -10
                    character.tryingmoveleft = True
                if event.key == K_w:
                    cont = False
                    for event2 in event_list:
                        if event2.type == KEYDOWN and event2.key == K_s:
                            cont = True
                    if cont: continue
                    character.movepos[1] = -10
                    character.tryingmoveup = True
                if event.key == K_s:
                    cont = False
                    for event2 in event_list:
                        if event2.type == KEYDOWN and event2.key == K_w:
                            cont = True
                    if cont: continue
                    character.movepos[1] = 10
                    character.tryingmovedown = True
                if event.key == K_d:
                    cont = False
                    for event2 in event_list:
                        if event2.type == KEYDOWN and event2.key == K_a:
                            cont = True
                    if cont: continue
                    character.movepos[0] = 10
                    character.tryingmoveright = True
            elif event.type == KEYUP:
                if event.key == K_a:
                    #if character.movepos[0] < 0:
                    if character.tryingmoveright == False:
                        character.movepos[0] = 0
                    else:
                        character.movepos[0] = 10
                    character.tryingmoveleft = False
                if event.key == K_w:
                    #if character.movepos[1] < 0:
                    if character.tryingmovedown == False:
                        character.movepos[1] = 0
                    else:
                        character.movepos[1] = 10
                    character.tryingmoveup = False
                if event.key == K_s:
                    #if character.movepos[1] > 0:
                    if character.tryingmoveup == False:
                        character.movepos[1] = 0
                    else:
                        character.movepos[1] = -10
                    character.tryingmovedown = False
                if event.key == K_d:
                    #if character.movepos[0] > 0:
                    if character.tryingmoveleft == False:
                        character.movepos[0] = 0
                    else:
                        character.movepos[0] = -10
                    character.tryingmoveright = False
        screen.blit(background, character.rect)
        charactersprites.update()
        charactersprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()