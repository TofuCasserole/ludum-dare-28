'''
Created on Dec 15, 2013

@author: kristoffe
'''

import math
import os
import pygame

def distance(coorda, coordb):
    w = coorda[0] + coordb[0]
    h = coorda[1] + coordb[1]
    return math.sqrt(w*w + h*h)

def convert_to_unit_vector(x1, x2, y1, y2):
    x_distance = abs(x1 - x2)
    y_distance = abs(y1 - y2)
    x_speed = float(x_distance)/float(x_distance+y_distance)
    y_speed = float(y_distance)/float(x_distance+y_distance)
    if x1 > x2:
        x_speed *= -1
    if y1 > y2:
        y_speed *= -1
    return (x_speed, y_speed)

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('../', 'res', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
    return image