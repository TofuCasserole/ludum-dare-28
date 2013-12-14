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
    
    model.initrooms()
    dirt = model.load_png("dirt.png")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    for x in range(32,640,32):
        for y in range(0,480,32):
            background.blit(dirt[0], (x,y))
        
    character = model.Character()
    
    
    clock = pygame.time.Clock()
    
    charactersprites = pygame.sprite.RenderUpdates(character)
    
    obstacles = pygame.sprite.RenderPlain()
    obstacles.add(model.Obstacle((128,128), "rock.png"), model.Obstacle((128, 192), "rock.png"), model.Obstacle((192,192), "rock.png"))
    
    monsters = pygame.sprite.RenderPlain()
    monsters.add(model.Monster(charactersprites, obstacles, monsters), model.Monster(charactersprites, obstacles, monsters))
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    while True:
        clock.tick(30)
        event_list = [event for event in pygame.event.get()]
        for event in event_list:
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if True == False:
                    pass
                elif event.key == K_a:
                    cont = False
                    for event2 in event_list:
                        if event2.type == KEYDOWN and event2.key == K_d:
                            cont = True
                    if cont: continue
                    character.movepos[0] = -8
                    character.tryingmoveleft = True
                elif event.key == K_w:
                    cont = False
                    for event2 in event_list:
                        if event2.type == KEYDOWN and event2.key == K_s:
                            cont = True
                    if cont: continue
                    character.movepos[1] = -8
                    character.tryingmoveup = True
                elif event.key == K_s:
                    cont = False
                    for event2 in event_list:
                        if event2.type == KEYDOWN and event2.key == K_w:
                            cont = True
                    if cont: continue
                    character.movepos[1] = 8
                    character.tryingmovedown = True
                elif event.key == K_d:
                    cont = False
                    for event2 in event_list:
                        if event2.type == KEYDOWN and event2.key == K_a:
                            cont = True
                    if cont: continue
                    character.movepos[0] = 8
                    character.tryingmoveright = True
            elif event.type == KEYUP:
                if True == False:
                    pass
                elif event.key == K_a:
                    #if character.movepos[0] < 0:
                    if character.tryingmoveright == False:
                        character.movepos[0] = 0
                    else:
                        character.movepos[0] = 8
                    character.tryingmoveleft = False
                elif event.key == K_w:
                    #if character.movepos[1] < 0:
                    if character.tryingmovedown == False:
                        character.movepos[1] = 0
                    else:
                        character.movepos[1] = 8
                    character.tryingmoveup = False
                elif event.key == K_s:
                    #if character.movepos[1] > 0:
                    if character.tryingmoveup == False:
                        character.movepos[1] = 0
                    else:
                        character.movepos[1] = -8
                    character.tryingmovedown = False
                elif event.key == K_d:
                    #if character.movepos[0] > 0:
                    if character.tryingmoveleft == False:
                        character.movepos[0] = 0
                    else:
                        character.movepos[0] = -8
                    character.tryingmoveright = False
        screen.blit(background, (0,0))
        for monster in monsters.sprites():
            screen.blit(monster.image, monster.rect)
        charactersprites.update(obstacles, monsters)
        charactersprites.draw(screen)
        monsters.update(obstacles, monsters, character)
        monsters.draw(screen)
        obstacles.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()