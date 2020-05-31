#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pygame
from pygame.locals import QUIT, Rect


def make_line(num, prime, w_h):
    """各数値が素数か否かの情報を格納した１次元配列を生成"""
    line = np.empty(w_h*w_h, dtype=object)
    for i in range(num):
        data = {'num': i, "flag": 1 if i in prime else 0}
        line[i] = data
    return line


def make_arr(num, w_h, center, line):
    """0を中央とし逆時計回りに各数値を配置した２次元配列の生成"""
    #後のif文を回すために行、列ともに1ずつ大きな配列を作る
    arr = np.empty((w_h+1, w_h+1), dtype=object)
    # 0, 1, 2 は予め配置しておく
    arr[center[0]][center[1]] = line[0]
    arr[center[0]][center[1]+1] = line[1]
    arr[center[0]-1][center[1]+1] = line[2]

    now = (center[0]-1, center[1]+1)

    for i in range(3, num):
        if arr[now[0]][now[1]-1] is None and \
          arr[now[0]+1][now[1]] is not None:
            arr[now[0]][now[1]-1] = line[i]
            now = (now[0], now[1]-1)
        elif arr[now[0]+1][now[1]] is None and \
          arr[now[0]][now[1]+1] is not None:
            arr[now[0]+1][now[1]] = line[i]
            now = (now[0]+1, now[1])
        elif arr[now[0]][now[1]+1] is None and \
          arr[now[0]-1][now[1]] is not None:
            arr[now[0]][now[1]+1] = line[i]
            now = (now[0], now[1]+1)
        elif arr[now[0]-1][now[1]] is None and \
          arr[now[0]][now[1]-1] is not None:
            arr[now[0]-1][now[1]] = line[i]
            now = (now[0]-1, now[1])

    # 不要な行、列の削除
    arranged_arr = np.delete(np.delete(arr, w_h, 0), w_h, 1)
    return arranged_arr


def make_grid(num, prime):
    """描画の元となる配列を作成するための各関数の呼び出し"""
    w_h = int(np.ceil(np.sqrt(num)))
    wh_half = w_h // 2
    center = (wh_half, wh_half) if w_h**2 % 2 == 1 \
                            else (wh_half, wh_half - 1)

    line = make_line(num, prime, w_h)
    arr = make_arr(num, w_h, center, line)
    return arr


def choice_prime_num(arr):
    """np.array(0, num)を受け取って素数の配列を返す"""
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    if 0 in arr:
        arr.remove(0)
    if 1 in arr:
        arr.remove(1)
    prime = []
    _min = min(arr)
    _max = max(arr)
    while _min <= np.sqrt(_max):
        _min = min(arr)
        prime.append(_min)
        for i in arr:
            if i != _min and i % _min == 0:
                arr.remove(i)
        arr.remove(_min)
    prime.extend(arr)

    return prime


def draw(grid):
    """draw grid"""
    window_size = 600
    pygame.init()
    surface = pygame.display.set_mode((window_size, window_size))
    fpsclock = pygame.time.Clock()
    surface.fill((255, 255, 255))
    sysfont = pygame.font.SysFont(None, 20)

    colors = ((0, 255, 255), (255, 120, 0), (0, 0, 0))
    row, col = grid.shape
    size = window_size // row

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        for i in range(row):
            for j in range(col):
                color_num = grid[i][j]['flag'] \
                if grid[i][j] is not None else 2
                pygame.draw.rect(surface,
                                 colors[color_num],
                                 Rect(j*size, i*size, size, size))
                text = str(grid[i][j]['num']) if grid[i][j] is not None else '-'
                cell_num = sysfont.render(text, False, (105, 105, 105))
                surface.blit(cell_num, (j*size, i*size))
        pygame.display.update()
        fpsclock.tick(10)


if __name__ == '__main__':
    NUM = 256
    prime = choice_prime_num(np.arange(0, NUM))
    grid = make_grid(NUM, prime)
    draw(grid)
