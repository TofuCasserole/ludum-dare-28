'''
Created on Dec 13, 2013

@author: thedoctor
'''

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"

import model

def move_character(character, direction):
    (xpos, ypos) = character.location
    if direction == LEFT and (xpos-1, ypos) not in character.room.obstacles:
        if (xpos-1, ypos) in character.room.monster_locations():
            character.health -= 20
            return
        if (xpos == 0 and model.EAST in character.room.doors):
            
        character.loation = (xpos-1,ypos)
        return
    if direction == RIGHT and xpos < model.WIDTH and (xpos+1, ypos) not in character.room.obstacles:
        if (xpos+1, ypos) in character.room.monster_locations():
            character.health -= 20
            return
        character.loation = (xpos+1,ypos)
        return
    if direction == UP and ypos > 0 and (xpos, ypos - 1) not in character.room.obstacles:
        if (xpos, ypos-1) in character.room.monster_locations():
            character.health -= 20
            return
        character.loation = (xpos,ypos - 1)
        return
    if direction == DOWN and ypos < model.LENGTH and (xpos, ypos - 1) not in character.room.obstacles:
        if (xpos, ypos+1) in character.room.monster_locations():
            character.health -= 20
            return
        character.loation = (xpos,ypos - 1)
        return