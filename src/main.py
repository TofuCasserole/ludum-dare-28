'''
Created on Dec 13, 2013

@author: kristoffe
'''
import pygame
from pygame.locals import *
import model
import gui

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    
    dirt = model.load_png("dirt.png")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    for x in range(32,640,32):
        for y in range(0,480,32):
            background.blit(dirt[0], (x,y))
    
    l=model.Level()    
    character = model.Character()
    
    healthbar = gui.HealthBar()
    
    clock = pygame.time.Clock()
    
    charactersprites = pygame.sprite.RenderUpdates(character)
    
    obstacles = pygame.sprite.RenderPlain()
    obstacles.add(model.Obstacle((128,128), "rock.png"), model.Obstacle((128, 192), "rock.png"), model.Obstacle((192,192), "rock.png"))
    
    monsters = pygame.sprite.RenderUpdates()
    monsters.add(model.Monster(charactersprites, obstacles, monsters), model.Monster(charactersprites, obstacles, monsters))
    
    sword = pygame.sprite.RenderUpdates()

    moveables = pygame.sprite.RenderUpdates()
    moveables.add(monsters.sprites(), character)
    
    currentroom = l.rootRoom
    obstacles.add(currentroom.walls)
    
    while True:
        clock.tick(40)
        event_list = [event for event in pygame.event.get()]
        for event in event_list:
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if sword.sprites() == [] and character.sword_cooldown > 25:
                    sword.add(model.Sword(character))
            elif event.type == KEYDOWN:
                if True == False:
                    pass
                elif event.key == K_a:
                    cont = False
                    for event2 in event_list:
                        if event2.type == KEYDOWN and event2.key == K_d:
                            cont = True
                    if cont: continue
                    character.movepos[0] = -6
                    character.tryingmoveleft = True
                    character.last_direction_moved = "left"
                elif event.key == K_w:
                    cont = False
                    for event2 in event_list:
                        if event2.type == KEYDOWN and event2.key == K_s:
                            cont = True
                    if cont: continue
                    character.movepos[1] = -6
                    character.tryingmoveup = True
                    character.last_direction_moved = "up"
                elif event.key == K_s:
                    cont = False
                    for event2 in event_list:
                        if event2.type == KEYDOWN and event2.key == K_w:
                            cont = True
                    if cont: continue
                    character.movepos[1] = 6
                    character.tryingmovedown = True
                    character.last_direction_moved = "down"
                elif event.key == K_d:
                    cont = False
                    for event2 in event_list:
                        if event2.type == KEYDOWN and event2.key == K_a:
                            cont = True
                    if cont: continue
                    character.movepos[0] = 6
                    character.tryingmoveright = True
                    character.last_direction_moved = "right"
            elif event.type == KEYUP:
                if True == False:
                    pass
                elif event.key == K_a:
                    #if character.movepos[0] < 0:
                    if character.tryingmoveright == False:
                        character.movepos[0] = 0
                    else:
                        character.movepos[0] = 6
                    character.tryingmoveleft = False
                elif event.key == K_w:
                    #if character.movepos[1] < 0:
                    if character.tryingmovedown == False:
                        character.movepos[1] = 0
                    else:
                        character.movepos[1] = 6
                    character.tryingmoveup = False
                elif event.key == K_s:
                    #if character.movepos[1] > 0:
                    if character.tryingmoveup == False:
                        character.movepos[1] = 0
                    else:
                        character.movepos[1] = -6
                    character.tryingmovedown = False
                elif event.key == K_d:
                    #if character.movepos[0] > 0:
                    if character.tryingmoveleft == False:
                        character.movepos[0] = 0
                    else:
                        character.movepos[0] = -6
                    character.tryingmoveright = False
        screen.blit(background, (0,0))
        healthbar.draw(screen)
        currentroom.walls.draw(screen)
        for monster in currentroom.monsters.sprites():
            screen.blit(monster.image, monster.rect)
        charactersprites.update(obstacles, moveables)
        sword.update(character, monsters)
        charactersprites.draw(screen)
        monsters.update(obstacles, moveables, character)
        monsters.draw(screen)
        obstacles.draw(screen)
        currentroom.door_sprites.update(character)
        sword.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
