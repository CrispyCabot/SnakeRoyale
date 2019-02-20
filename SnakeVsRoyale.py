#SnakeVs.py
import pygame
import os
import math
from random import randint
from pygame.locals import *

pygame.init()

width = 800
height = 500
size = 10
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake Royale")

PATH = os.path.abspath(__file__)
PATH = PATH[0:-16] #-10 to chop off SnakeVs.py
font = pygame.font.Font(os.path.join(PATH,'font.ttf'), 36)

clock = pygame.time.Clock()

class Snake:
    def __init__(self, pos, dir, name):
        self.bod = [] #Lists [[x,y], [x,y]...]
        self.dir = dir #String 'direction'
        self.pos = pos #List [x,y]
        self.name = name #Name 'Chris'
        self.length = 1
    def getInfo(self):
        return [self.bod, self.dir, self.pos]
    def setDir(self, info):
        self.dir = getattr(playerUpdates, self.name)(self.pos, self.bod, self.dir, info)
    def update(self, win):
        if self.dir == 'right':
            self.pos[0]+=size
        elif self.dir == 'left':
            self.pos[0]-=size
        elif self.dir == 'up':
            self.pos[1]-=size
        elif self.dir == 'down':
            self.pos[1]+=size
        else:
            print("No direction set", self.name)
        self.bod.append([self.pos[0], self.pos[1]])
        if len(self.bod) > self.length:
            self.bod.pop(0)
        for i in self.bod:
            pygame.draw.rect(win, (0,255,0), pygame.Rect(i[0], i[1], size, size))
        #Check for hit

def main():
    players = ['Chris']
    snakeList = []
    info = []

    dirs = ['right', 'left', 'up', 'down']
    for i in players:
        x = randint(0,(width/size))*size
        y = randint(0,(height/size))*size
        snake = Snake([x, y], dirs[randint(0,3)], i)
        snakeList.append(snake)

    end = True
    playing = True
    while playing:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False

        info = []
        for i in snakeList:
            i.setDir(info)
            info.append(i.getInfo())

        #Draw everything
        pygame.draw.rect(win, (0,0,0), pygame.Rect(0,0,width,height))
        for i in snakeList:
            i.update(win)
        pygame.draw.rect(win, (255,255,255), pygame.Rect(0,0,width,height), 1) #White border
        pygame.display.update()

    while end: #This is just so it doesn't immediately close after someone loses
        clock.tick(size)
        for event in pygame.event.get():
            if event.type == QUIT:
                end = False
        keys = pygame.key.get_pressed()
        for i in keys:
            if i:
                end = False
        #Draw everything - identical to above
        pygame.draw.rect(win, (0,0,0), pygame.Rect(0,0,width,height)) #Background

        for i in bod1:
            pygame.draw.rect(win, (255,0,0), pygame.Rect(i[0],i[1],size,size))
        pygame.draw.rect(win, (255,0,0), pygame.Rect(x1,y1,size,size))
        for i in bod2:
            pygame.draw.rect(win, (0,255,0), pygame.Rect(i[0],i[1],size,size))
        pygame.draw.rect(win, (0,255,0), pygame.Rect(x2,y2,size,size))

        if p1lose:
            pygame.draw.rect(win, (255,255,0), pygame.Rect(x1,y1,size,size))
        if p2lose:
            pygame.draw.rect(win, (255,255,0), pygame.Rect(x2,y2,size,size))
        if p1lose:
            pygame.draw.rect(win, (255,255,0), pygame.Rect(x1,y1,size,size))
            text = font.render("Player 2 Wins (Green)", True, (255,255,0))
            loc = text.get_rect()
            loc.center = (width/2, height/2)
            win.blit(text, loc)
        if p2lose:
            pygame.draw.rect(win, (255,255,0), pygame.Rect(x2,y2,size,size))
            text = font.render("Player 1 Wins (Red)", True, (255,255,0))
            loc = text.get_rect()
            loc.center = (width/2, height/2)
            win.blit(text, loc)
        pygame.display.update()
    pygame.quit()

class playerUpdates:
    def Chris(pos, bod, dir, info):
        newX, newY = pos[0], pos[1]
        if dir == 'right':
            newX += size
        if dir == 'left':
            newX -= size
        if dir == 'up':
            newY -= size
        if dir == 'down':
            newY += size

        if newX >= width:
            return 'up'
        if newX < 0:
            return 'down'
        if newY >= height:
            return 'right'
        if newY < 0:
            return 'left'
        return dir
main()
