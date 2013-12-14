'''
Created on Dec 13, 2013

@author: thedoctor
'''

class Character:
    def __init__(self, location, start_room):
        self.location = location
        self.health = 100
        self.room = start_room