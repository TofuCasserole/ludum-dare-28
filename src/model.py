'''
Created on Dec 13, 2013

@author: thedoctor
'''
DALEK = 0
CYBERMAN = 1
WEEPINGANGELS = 2
SILENCE = 3

EAST = "east"
WEST = "west"
NORTH = "north"
SOUTH = "south"

LENGTH = 9
WIDTH = 13

import os
import random
import pygame
from pygame.locals import *

#WOOOOOOO!!!!

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('../', 'res', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = pygame.transform.scale(image.convert(), (32, 32))
        else:
            image = pygame.transform.scale(image.convert_alpha(), (32, 32))
    except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
    return image, image.get_rect()

class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('char.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.health = 100
        #self.room = start_room
        self.movepos = [0,0]
        self.tryingmoveright = False
        self.tryingmoveleft = False
        self.tryingmoveup = False
        self.tryingmovedown = False
        self.last_direction_moved = "right"
        self.state = "move"
        self.hitcount = 0
        self.invuln_count = 0
        self.hitmove = [0,0]
        
    def update(self, obstacles, monsters):
        if self.state == "hit":
            if self.hitcount < 30:
                self.hitcount += 1
            else:
                self.state = "invulnerable"
                self.hitcount = 0
        
            newpos = self.rect.move([self.hitmove[0], 0])
            if self.area.contains(newpos):
                self.rect = newpos
                for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
                    if self.hitmove[0] > 0 and self.rect.right > obstacle.rect.left:
                        self.rect.right = obstacle.rect.left
                    if self.hitmove[0] < 0 and self.rect.left < obstacle.rect.right:
                        self.rect.left = obstacle.rect.right
            
            
            newpos = self.rect.move([0, self.hitmove[1]])
            if self.area.contains(newpos):
                self.rect = newpos
                for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
                    if self.hitmove[1] > 0 and self.rect.bottom > obstacle.rect.top:
                        self.rect.bottom = obstacle.rect.top
                    if self.hitmove[1] < 0 and self.rect.top < obstacle.rect.bottom:
                        self.rect.top = obstacle.rect.bottom
            pygame.event.pump()
            return
        
        if self.state == "invulnerable":
            if self.invuln_count < 20:
                self.invuln_count += 1
            else:
                self.invuln_count = 0
                self.state = "move"
        
        newpos = self.rect.move([self.movepos[0], 0])
        if self.area.contains(newpos):
            self.rect = newpos
        for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
            if self.movepos[0] > 0 and self.rect.right > obstacle.rect.left:
                self.rect.right = obstacle.rect.left
            if self.movepos[0] < 0 and self.rect.left < obstacle.rect.right:
                self.rect.left = obstacle.rect.right
        #if self.state == "invulnerable":
        for obstacle in pygame.sprite.spritecollide(self, monsters, 0):
            if self.movepos[0] > 0 and self.rect.right > obstacle.rect.left:
                self.rect.right = obstacle.rect.left
            if self.movepos[0] < 0 and self.rect.left < obstacle.rect.right:
                self.rect.left = obstacle.rect.right
            
        newpos = self.rect.move([0, self.movepos[1]])
        if self.area.contains(newpos):
            self.rect = newpos
        for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
            if self.movepos[1] > 0 and self.rect.bottom > obstacle.rect.top:
                self.rect.bottom = obstacle.rect.top
            if self.movepos[1] < 0 and self.rect.top < obstacle.rect.bottom:
                self.rect.top = obstacle.rect.bottom
        #if self.state == "invulnerable":
        for obstacle in pygame.sprite.spritecollide(self, monsters, 0):
            if self.movepos[1] > 0 and self.rect.bottom > obstacle.rect.top:
                self.rect.bottom = obstacle.rect.top
            if self.movepos[1] < 0 and self.rect.top < obstacle.rect.bottom:
                self.rect.top = obstacle.rect.bottom
        pygame.event.pump()
        

class Monster(pygame.sprite.Sprite):
    def __init__(self, character, obstacles, monsters):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('slime.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        random.seed()
        self.rect.topleft = (random.randint(0,self.area.right-64), random.randint(0,self.area.bottom-64))
        while (pygame.sprite.spritecollide(self, character, 0) != [] or pygame.sprite.spritecollide(self, obstacles, 0) != []
               or pygame.sprite.spritecollide(self, monsters, 0) != []):
            self.rect.topleft = (random.randint(0,self.area.right), random.randint(0,self.area.bottom))
        self.state = "chase"
        self.movepos = [0,0]
        self.hitcount = 0
        
    def update(self, obstacles, monsters, character):
        if self.state == "hit":
            if self.hitcount < 30:
                self.hitcount += 1
            else:
                self.hitcount = 0
                self.state = "chase"
                
        if self.state == "chase":
            self.moveclock = 0
            if self.rect.top > character.rect.top:
                self.movepos[1] = -2
            elif self.rect.bottom < character.rect.bottom:
                self.movepos[1] = 2
            else:
                self.movepos[1] = 0
            if self.rect.left > character.rect.left:
                self.movepos[0] = -2
            elif self.rect.right < character.rect.right:
                self.movepos[0] = 2
            else:
                self.movepos[0] = 0
                
        newpos = self.rect.move([self.movepos[0], 0])
        if self.area.contains(newpos):
            self.rect = newpos
        for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
            if obstacle == self:
                continue
            if self.movepos[0] > 0 and self.rect.right > obstacle.rect.left:
                self.rect.right = obstacle.rect.left
                for monster in pygame.sprite.spritecollide(self, monsters, 0):
                    if monster == self:
                        continue
                    if self.rect.left < monster.rect.right:
                        monster.rect.right = self.rect.left
            if self.movepos[0] < 0 and self.rect.left < obstacle.rect.right:
                self.rect.left = obstacle.rect.right
                for monster in pygame.sprite.spritecollide(self, monsters, 0):
                    if monster == self:
                        continue
                    if self.rect.right > monster.rect.left:
                        monster.rect.left = self.rect.right
        if self.state != "hit":
            for obstacle in pygame.sprite.spritecollide(self, monsters, 0):
                if obstacle == self:
                    continue
                if self.movepos[0] > 0 and self.rect.right > obstacle.rect.left:
                    self.rect.right = obstacle.rect.left
                    for monster in pygame.sprite.spritecollide(self, monsters, 0):
                        if monster == self:
                            continue
                        if self.rect.left < monster.rect.right:
                            monster.rect.right = self.rect.left
                if self.movepos[0] < 0 and self.rect.left < obstacle.rect.right:
                    self.rect.left = obstacle.rect.right
                    for monster in pygame.sprite.spritecollide(self, monsters, 0):
                        if monster == self:
                            continue
                        if self.rect.right > monster.rect.left:
                            monster.rect.left = self.rect.right
        if self.state == "hit":
            for obstacle in pygame.sprite.spritecollide(self, monsters, 0):
                if obstacle == self:
                    continue
                if self.movepos[0] > 0 and self.rect.right > obstacle.rect.left:
                    obstacle.state = "hit"
                    obstacle.hitcount = self.hitcount
                    obstacle.movepos[0] = self.movepos[0]
                    obstacle.rect.left = self.rect.right
                if self.movepos[0] < 0 and self.rect.left < obstacle.rect.right:
                    obstacle.state = "hit"
                    obstacle.hitcount = self.hitcount
                    obstacle.movepos[0] = self.movepos[0]
                    obstacle.rect.right = self.rect.left
        
        if pygame.sprite.collide_rect(self, character) and self.state != "hit" and character.state != "invulnerable":
            character.state = "hit"
            character.hitmove[0] = self.movepos[0]/2
            character.hitmove[1] = self.movepos[1]/2
            self.state = "hit"
            if self.movepos[0] > 0:
                self.rect.right = character.rect.left
                for monster in pygame.sprite.spritecollide(self, monsters, 0):
                    if monster == self:
                        continue
                    if self.rect.left < monster.rect.right:
                        monster.rect.right = self.rect.left
            if self.movepos[0] < 0:
                self.rect.left = character.rect.right
                for monster in pygame.sprite.spritecollide(self, monsters, 0):
                    if monster == self:
                        continue
                    if self.rect.right > monster.rect.left:
                        monster.rect.left = self.rect.right
            self.movepos[0] *=  -1/2
            self.movepos[1] *= -1/2
        elif pygame.sprite.collide_rect(self, character):
            self.state = "hit"
            self.movepos[0] *=  -1/2
            self.movepos[1] *= -1/2
            
        newpos = self.rect.move([0, self.movepos[1]])
        if self.area.contains(newpos):
            self.rect = newpos
        for obstacle in pygame.sprite.spritecollide(self, obstacles, 0):
            if obstacle == self:
                continue
            if self.movepos[1] > 0 and self.rect.bottom > obstacle.rect.top:
                self.rect.bottom = obstacle.rect.top
                for monster in pygame.sprite.spritecollide(self, monsters, 0):
                    if monster == self:
                        continue
                    if self.rect.top < monster.rect.bottom:
                        monster.rect.bottom = self.rect.top
            if self.movepos[1] < 0 and self.rect.top < obstacle.rect.bottom:
                self.rect.top = obstacle.rect.bottom
                for monster in pygame.sprite.spritecollide(self, monsters, 0):
                    if monster == self:
                        continue
                    if self.rect.bottom > monster.rect.top:
                        monster.rect.top = self.rect.bottom
        if self.state != "hit":
            for obstacle in pygame.sprite.spritecollide(self, monsters, 0):
                if obstacle == self:
                    continue
                if self.movepos[1] > 0 and self.rect.bottom > obstacle.rect.top:
                    self.rect.bottom = obstacle.rect.top
                    for monster in pygame.sprite.spritecollide(self, monsters, 0):
                        if monster == self:
                            continue
                        if self.rect.top < monster.rect.bottom:
                            monster.rect.bottom = self.rect.top
                if self.movepos[1] < 0 and self.rect.top < obstacle.rect.bottom:
                    self.rect.top = obstacle.rect.bottom
                    for monster in pygame.sprite.spritecollide(self, monsters, 0):
                        if monster == self:
                            continue
                        if self.rect.bottom > monster.rect.top:
                            monster.rect.top = self.rect.self
        if self.state == "hit":
            for obstacle in pygame.sprite.spritecollide(self, monsters, 0):
                if obstacle == self:
                    continue
                if obstacle.movepos[1] > 0 and self.rect.bottom > obstacle.rect.top:
                    obstacle.state = "hit"
                    obstacle.hitcount = self.hitcount
                    obstacle.movepos[1] = self.movepos[1]
                    obstacle.rect.top = self.rect.bottom
                if self.movepos[1] < 0 and self.rect.top < obstacle.rect.bottom:
                    obstacle.state = "hit"
                    obstacle.hitcount = self.hitcount
                    obstacle.movepos[1] = self.movepos[1]
                    obstacle.rect.bottom = self.rect.top
        if pygame.sprite.collide_rect(self, character) and self.state != "hit" and character.state != "invulnerable":
            character.state = "hit"
            character.hitmove[0] = self.movepos[0]/2
            character.hitmove[1] = self.movepos[1]/2
            self.state = "hit"
            if self.movepos[1] > 0:
                self.rect.bottom =  character.rect.top
                for monster in pygame.sprite.spritecollide(self, monsters, 0):
                    if monster == self:
                        continue
                    if self.rect.top < monster.rect.bottom:
                        monster.rect.bottom = self.rect.top
            if self.movepos[1] < 0:
                self.rect.top = character.rect.bottom
                for monster in pygame.sprite.spritecollide(self, monsters, 0):
                    if monster == self:
                        continue
                    if self.rect.bottom > monster.rect.top:
                        monster.rect.top = self.rect.bottom
            self.movepos[0] *=  -1/2
            self.movepos[1] *= -1/2
        elif pygame.sprite.collide_rect(self, character):
            self.state = "hit"
            self.movepos[0] *=  -1/2
            self.movepos[1] *= -1/2
        pygame.event.pump()

class Sword(pygame.sprite.Sprite):
    def __init(self, character):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('sword.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        if character.last_direction_moved == "right":
            self.rect.midleft = character.rect.midright
        if character.last_direction_moved == "left":
            self.rect.midright = character.rect.midleft
        if character.last_direction_moved == "up":
            self.rect.midbottom = character.rect.midtop
        if character.last_direction_moved == "down":
            self.rect.midtop = character.rect.midbottom
        self.count = 0
        
    def update(self, character):
        if self.count > 20:
            self.kill()
            return
        if character.last_direction_moved == "right":
            self.rect.midleft = character.rect.midright
        if character.last_direction_moved == "left":
            self.rect.midright = character.rect.midleft
        if character.last_direction_moved == "up":
            self.rect.midbottom = character.rect.midtop
        if character.last_direction_moved == "down":
            self.rect.midtop = character.rect.midbottom
        self.count += 1

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, location, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(sprite)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = location
'''
doors are passed as an array of "east", "north", "south", and "west"

obstacles are passed as a list array of 2 tuples with the y parameter first and the x
parameter second, starting at 0,0 in the top left corner e.g.,
-------------------
| 0,0 | 0,1 | 0,2 |
-------------------
| 1,0 | 1,1 | 1,2 |
-------------------
| 2,0 | 2,1 | 2,2 |
-------------------

unlocated monster objects are passed as an array on construction
'''
random.seed()

def move(sprite, moveables, obstacles, movepos, reallign = False):
    oldpos = sprite.rect
    newpos = sprite.rect.move[(movepos[0], 0)]
    if sprite.area.contains(newpos) and not reallign:
        sprite.rect = newpos
    for obstacle in pygame.sprite.spritecollide(sprite, obstacles):
        if movepos[0] > 0 and sprite.rect.right > obstacle.rect.left:
            sprite.rect.right = obstacle.rect.left
            for moveable in pygame.sprite.spritecollide(sprite, moveables, 0):
                move(moveable, moveables, obstacles, moveable.getmovepos(), True)
        if movepos[0] < 0 and sprite.rect.left < obstacle.rect.right:
            sprite.rect.left = obstacle.rect.right
            for moveable in pygame.sprite.spritecollide(sprite, moveables, 0):
                move(moveable, moveables, obstacles, moveable.getmovepos(), True)
    for moveable in pygame.sprite.spritecollide(sprite, moveables):
        if moveable == sprite:
            continue
        if movepos[0] > sprite.rect.right > moveable.left:
            sprite.rect.right = moveable.rect.left
            sprite.on_collision(moveable)
            for moveable in pygame.sprite.spritecollide(sprite, moveables, 0):
                move(moveable, moveables, moveable.getmovepos(), True)
            
        
    
        
        

class Room:
    def __init__(self, cord,doors=[], obstacles=None, monsters=None):
        self.doors = doors
        self.connectingRooms={}#door:room -> NORTH:<roomObject>
        self.obstacles = obstacles
        self.monsters = monsters
        self.cord=cord
    def __str__(self):
        return str(self.cord)+':'+str(self.connectingRooms)
    def __repr__(self):
        return self.__str__()
        '''
        possible_locations = [(x,y) for x in range(0, WIDTH) for y in range (0, LENGTH) if (x,y) not in self.obstacles]
        random.shuffle(possible_locations)
        for monster in self.monsters:
            monster.location = possible_locations.pop()
        self.walls = pygame.sprite.RenderPlain()
        # generate north/south walls
        for x in range(32, 640, 32):
            if not (x == 320 and NORTH in doors):
                self.walls.add(Obstacle((x, 0), "wall.png"))
            if not (x == 320 and SOUTH in doors):
                self.walls.add(Obstacle((x, 448), "wall.png"))
        # generate east/west walls
        for y in range(0, 480, 32):
            if not (y == 224 and WEST in doors):
                self.walls.add(Obstacle((32, y), "wall.png"))
            if not (y == 224 and EAST in doors):
                self.walls.add(Obstacle((608, y), "wall.png"))
                
    def initConnectingRooms(self):
        for door in self.doors:
            self.connectingRooms[door]=''
    def monster_locations(self):
        return [monster.location for monster in self.monsters]
    '''
cur_room_row = 0
cur_room_col = 0

'''
The level class contains all of the rooms for this specific level in a linked list
'''
class Level:
    def __init__(self):
        self.directions={0:'NORTH',1:'SOUTH',2:'EAST',3:'WEST'}
        #self.cords={}#cord:[exit cords]
        #figure out how many rooms we are going to generate
        self.numberOfRooms=random.randint(10,15)
        #generate the cords of the rooms
        print 'generating cords'
        cords=self.__generateCords()
        while cords==None:
            print 'generating cords'
            cords=self.__generateCords()
        #print len(cords)
        #print cords
        #convert the cords to rooms and make them a self contained graph
        self.rootRoom=''
        self.__generateRooms(cords)
    def __generateCords(self,cords={},queue=[]):
        if len(cords)>=self.numberOfRooms:
            return cords
        if len(cords)==0:
            cords[(0,0)]=[]#generate the init cord with no exits
            currentCord=(0,0)
        else:
            if len(queue)>0:
                currentCord=queue.pop(0)
            else:
                print len(cords)
                return None #we need to throw this one out and try again...
        #find some exits!
        exits=self.__generateExits(currentCord)
        #check to see if these cords already exits
        for exit in exits:
            if exit not in cords:
                cords[exit]=[currentCord]#room doesnt exist so lets add it and add the currentCord as an exit
                #since this is a new room lets add it to the queue!
                queue.append(exit)
            else:#since the cord already exits lets add the currentCord as an exit    
                cords[exit].append(currentCord) 
            cords[currentCord].append(exit)#append the exit the the current cord
        #time to call this function again!
        return self.__generateCords(cords, queue)
    def __generateExits(self, currentCord):
        exits=[]
        directions=[-1,1,1,-1]
        #0 north, 1 east, 2 south, 3 west
        for i in range(0,4):
            if bool(random.randint(0,1)):
                if i%2==0: #north or south Y cord
                    exits.append((currentCord[0],currentCord[1]+directions[i]))
                else: #east or west, X cord
                    exits.append((currentCord[0]+directions[i],currentCord[1]))
        return exits
    def __generateRooms(self,cords, currentCord=(0,0), currentRoom=None, rooms={}, visited=[]):
        #we need to traverse the cords to generate the rooms
        #start by creating the root room
        if currentCord==(0,0):
            self.rootRoom=Room(currentCord)
            currentRoom=self.rootRoom
            rooms[(0,0)]=self.rootRoom
        #time to iterate through all of the exits, create the rooms if needed, and connect them
        for exit in cords[currentCord]:
            direction=''
            #we need to figure out what direction this door is at
            if exit[0]>currentCord[0]:#exit is EAST
                direction='EAST'
            elif exit[0]<currentCord[0]:#exit is WEST
                direction='WEST'
            elif exit[1]>currentCord[1]:#exit is SOUTH
                direction='SOUTH'
            elif exit[1]<currentCord[1]:#exit is NORTH
               direction='NORTH'
            #add this to the doors list
            currentRoom.doors.append(direction)
            #check to see if a room exists, if not add it
            if exit not in rooms:
                rooms[exit]=Room(exit)
            currentRoom.connectingRooms[direction]=rooms[exit]
        #now that we have created some rooms lets go through each of the exits again and recurvsively create the rooms
        visited.append(currentCord)
        for exit in cords[currentCord]:
            if exit not in visited:
                self.__generateRooms(cords, exit, rooms[exit], rooms, visited)

    def __toString(self, room):
        s=''
        s+=room+':['
        for key in room.connectingRooms:
            pass
    def __str__(self):
        
        return self.rootRoom.__str__()
    def __repr__(self):
        self.__str__()
l=Level()
print l

