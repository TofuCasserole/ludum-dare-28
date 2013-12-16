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
    myFont = pygame.font.Font('../res/SWFIT_SL.TTF', 24)
    dirt = pygame.transform.scale2x(model.load_png("dirt.png"))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    for x in range(32,640,32):
        for y in range(0,480,32):
            background.blit(dirt, (x,y))
    levelNumber=1 
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
                if event.subtype=='BossDeath':
                    print 'boss death'
                    #clear out the boss door so that the player can roam around the level
                    l.getLocation(l.bossRoom).bossdoors.empty()
                    #l.getLocation(l.bossRoom).bossdoors=pygame.sprite.RenderPlain()
                    el=model.Elevator()
                    #l.getLocation(l.bossRoom).obstacles.add(el)
                    #l.getLocation(l.bossRoom).walls.add(el)
                    #print character.currentroom.moveables
                    #l.getLocation(l.bossRoom).bossdoors.add(el)
                    l.getLocation(l.bossRoom).levelExit.add(el)
                    #obstacles.add(el)
                if event.subtype=='ChangeLevel':
                    #now we have to start a new level!
                    levelNumber+=1
                    l=model.Level(levelNumber)
                    character.currentroom = l.getLocation(l.rootRoom)
                    for room in l.getAllRooms():
                        room.add_monsters(charactersprites, l)
                    obstacles.add(character.currentroom.walls)
                    continue
            elif event.type == KEYDOWN:
                if event.key == K_TAB:
                    alpha = pygame.Surface(screen.get_size())
                    alpha.fill((0,0,0))
                    alpha.set_alpha(128)
                    screen.blit(alpha, (0,0))
                    pygame.display.flip()
                    exit_inventory = False
                    while(1):
                        event_list = [event for event in pygame.event.get()]
                        for event in event_list:
                            if event.type == QUIT:
                                return
                            elif event.type == KEYDOWN:
                                if event.key == K_TAB:
                                    exit_inventory = True
                        if exit_inventory:
                            break
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
        character.currentroom.levelExit.draw(screen)
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
        character.currentroom.levelExit.update(character)
        sword.draw(screen)
        pygame.display.flip()
    alpha = pygame.Surface(screen.get_size())
    for x in range(64):
        clock.tick(32)
        alpha.fill((0,0,0))
        alpha.set_alpha(2)
        screen.blit(alpha, (0,0))
        pygame.display.flip()
    game_over = myFont.render("Game Over.", False, (255,0,0))
    screen.blit(game_over, (320,240))
    pygame.display.flip()
    while(1):    
        event_list = [event for event in pygame.event.get()]
        for event in event_list:
            if event.type == QUIT:
                return
if __name__ == '__main__':
    main()
