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

def text_format(surface, string, size, position, color = (66,66,66), maxlength = 30):
    font = pygame.font.Font("../res/SWFIT_SL.TTF", size)
    substring_list = []
    while len(string) > maxlength:
        substring_list.append(string[:maxlength])
        string = string[60:]
    substring_list.append(string)
    substring_objects = []
    for substring in substring_list:
        substring_objects.append(font.render(substring, False, color))
    for i in range(len(substring_objects)):
        surface.blit(substring_objects[i], (position[0],position[1]+i*font.get_linesize()))

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('../', 'res', name)
    try:
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
    except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
    return image
