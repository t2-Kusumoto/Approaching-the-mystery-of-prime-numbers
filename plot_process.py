#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame.locals import QUIT
import choice_prime_number as cpn

N = 400
size = np.arange(0, N)

prime = cpn.choice_prime_num(size)

#rad = np.e / 2*np.pi
#rad = np.e / np.e**(-2*np.pi)
rad = 2*np.pi / np.e
#rad = 2*np.pi**np.e / np.e**(-2*np.pi)
#rad = np.pi**np.e / np.e**(-np.pi)
#rad = np.pi**np.e / np.e**(np.pi)
radius = lambda a: np.sqrt(a)*np.e

data = np.empty(len(size), dtype=object)

plot_x = []
plot_y = []

for i in size:
    x = radius(i) * np.cos(rad*i)
    y = radius(i) * np.sin(rad*i)
    plot_x.append(x)
    plot_y.append(y)
    data[i] = {'num':i, 'point':(x, y)}

def draw(data, prime):
    """ draw grid"""
    window_size = 800
    pygame.init()
    surface = pygame.display.set_mode((window_size, window_size))
    fpsclock = pygame.time.Clock()
    surface.fill((255, 255, 255))
    sysfont = pygame.font.SysFont(None, 20)
    stock = []
    counter = 0
    colors = ((0,255,120),(255,0,0))


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if counter < N:
            stock.append(data[counter])

            for d in stock:
                x, y = d['point']
                x = int(np.round(x)*5)+400
                y = int(np.round(y)*5)+400
                text = str(d['num'])
                color = colors[0] if d['num'] in prime else colors[1]
                pygame.draw.circle(surface,color,(x,y),3)
                _num = sysfont.render(text, False, (105, 105, 105))
                surface.blit(_num, (x+3, y+3))

            time.sleep(0.3)

            counter += 1
        pygame.display.update()
        fpsclock.tick(10)

draw(data, prime)
