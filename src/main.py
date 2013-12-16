'''
Created on Dec 13, 2013

@author: kristoffe
'''
import pygame
from pygame.locals import *
import model
import gui
import utils

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    dirt = pygame.transform.scale2x(utils.load_png("dirt.png"))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    for x in range(32,640,32):
        for y in range(0,480,32):
            background.blit(dirt, (x,y))
    levelNumber=1 
    inventory = pygame.Surface((528,368))
    panel = pygame.surface.Surface((242, 32))
    panel.fill((192,192,192))
    selector = pygame.surface.Surface((246,36))
    selector.fill((255,0,255))
    l=model.Level(levelNumber)
    character = model.Character()
    
    healthbar = gui.HealthBar()
    
    clock = pygame.time.Clock()
    
    charactersprites = pygame.sprite.RenderUpdates(character)
    
    obstacles = pygame.sprite.RenderPlain()
    obstacles.add(model.Obstacle((128,128), "rock.png"), model.Obstacle((128, 192), "rock.png"), model.Obstacle((192,192), "rock.png"))
        
    sword = pygame.sprite.RenderUpdates()

    moveables = pygame.sprite.RenderUpdates()
    moveables.add(character)
    
    character.currentroom = l.getLocation(l.rootRoom)
    character.currentroom.moveables.add(character)
    
    for room in l.getAllRooms():
        room.add_monsters(charactersprites, l)
    
    obstacles.add(character.currentroom.walls)
    
    while True:
        clock.tick(40)
        event_list = [event for event in pygame.event.get()]
        for event in event_list:
            if event.type == QUIT:
                return
            elif event.type == USEREVENT:
                if event.subtype == "MonsterDeath":
                    l.num_monsters -= 1
                    print "Monsters Left", l.num_monsters   
                    if l.num_monsters == 0:
                        print("Level Clear!")
                        for room in l.getAllRooms():
                            if room.bossdoors.sprites() != []:
                                room.door_sprites.add(model.Door(room.bossdoors.sprites()[0].rect.topleft))
                                room.bossdoors.empty()
                elif event.subtype=='BossDeath':
                    #now we have to start a new level!
                    levelNumber+=1
                    l=model.Level(levelNumber)
                    character.currentroom = l.getLocation(l.rootRoom)
                    for room in l.getAllRooms():
                        room.add_monsters(charactersprites, l)
                    obstacles.add(character.currentroom.walls)
                    continue
            elif event.type == KEYDOWN:
                if event.key == K_i:
                    alpha = pygame.Surface(screen.get_size())
                    alpha.fill((0,0,0))
                    alpha.set_alpha(128)
                    screen.blit(alpha, (0,0))
                    pygame.display.flip()
                    exit_inventory = False
                    item_selected = 0
                    while(1):
                        inventory.fill((224,224,224))
                        inventory = inventory.convert()
                        utils.text_format(inventory, "INVENTORY", 24, (170,0), (0, 0, 255), 28)
                        utils.text_format(inventory, "Runes:", 16, (360, 34), (255,0,0),20)
                        utils.text_format(inventory, "Buffs:", 16, (100, 34), (255,0,255),20)
                        event_list = [event for event in pygame.event.get()]
                        for event in event_list:
                            if event.type == QUIT:
                                return
                            elif event.type == KEYDOWN:
                                if event.key == K_i:
                                    exit_inventory = True
                                elif event.key == K_DOWN:
                                    if (item_selected <7):
                                        item_selected += 1
                                elif event.key == K_UP:
                                    if (item_selected>0):
                                        item_selected -= 1  
                        if exit_inventory:
                            break
                        inventory.blit(selector, (270,62+36*item_selected))
                        for y in range(62,350,36):
                            inventory.blit(panel, (272, y+2))
                        for y in range(62,350,36):
                            inventory.blit(panel, (16, y+2))
                        screen.blit(inventory, (56,56))
                        pygame.display.flip()
                elif event.key == K_e:
                    for room in l.getAllRooms():
                        if room.medbay.sprites() != [] and room.medbay.sprites()[0].can_heal == True:
                            room.medbay.sprites()[0].is_healing = True
                elif event.key == K_SPACE or event.key == K_RETURN:
                    if sword.sprites() == [] and character.sword_cooldown > 10:
                        sword.add(model.Sword(character))
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
                if event.key == K_e:
                    for room in l.getAllRooms():
                        if room.medbay.sprites() != []:
                            room.medbay.sprites()[0].is_healing = False
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
        if character.health <= 0:
            break
        screen.blit(background, (0,0))
        healthbar.health = character.health
        healthbar.draw(screen)
        character.currentroom.walls.draw(screen)
        character.currentroom.monsters.draw(screen)
        character.currentroom.projectiles.draw(screen)
        character.currentroom.bossdoors.draw(screen)
        character.currentroom.medbay.draw(screen)
        #for monster in currentroom.monsters.sprites():
        #    screen.blit(monster.image, monster.rect)
        charactersprites.update(character.currentroom.walls, character.currentroom.moveables, sword)
        sword.update(character, character.currentroom.monsters)
        charactersprites.draw(screen)
        character.currentroom.projectiles.update(charactersprites)
        character.currentroom.bossdoors.update(character.currentroom.moveables)
        character.currentroom.monsters.update(character.currentroom.walls, character.currentroom.moveables, character)
        #obstacles.draw(screen)
        character.currentroom.door_sprites.update(character, l)
        character.currentroom.medbay.update(character)
        sword.draw(screen)
        pygame.display.flip()
    alpha = pygame.Surface(screen.get_size())
    for x in range(64):
        clock.tick(32)
        alpha.fill((0,0,0))
        alpha.set_alpha(2)
        screen.blit(alpha, (0,0))
        pygame.display.flip()
    utils.text_format(screen, "Game Over.", 24, (320, 240), (255, 0, 0), 15)
    pygame.display.flip()
    while(1):    
        event_list = [event for event in pygame.event.get()]
        for event in event_list:
            if event.type == QUIT:
                return
if __name__ == '__main__':
    main()
