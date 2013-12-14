'''
Created on Dec 13, 2013

@author: thedoctor
'''

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"

import Model.Room

def move_character(character, direction):
    (xpos, ypos) = character.location
    if direction == LEFT and xpos > 0 and (xpos-1, ypos) not in character.room.obstacles:
        if (xpos-1, ypos) in character.room.monster_locations():
            character.health -= 20
            return
        character.loation = (xpos-1,ypos)
        return
    if direction == RIGHT and xpos < Model.Room.WIDTH and (xpos+1, ypos) not in character.room.obstacles:
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
    if direction == DOWN and ypos < Model.Room.LENGTH and (xpos, ypos - 1) not in character.room.obstacles:
        if (xpos, ypos+1) in character.room.monster_locations():
            character.health -= 20
            return
        character.loation = (xpos,ypos - 1)
        return