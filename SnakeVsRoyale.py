#SnakeVs.py
import pygame
import os
import math
from random import randint
from pygame.locals import *
import time

pygame.init()

width = 800
height = 500
size = 10
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake Royale")

PATH = os.path.abspath(__file__)
PATH = PATH[0:-16] #-10 to chop off SnakeVs.py
font = pygame.font.SysFont('', 24)

clock = pygame.time.Clock()

length = 1

class Snake:
    global length
    def __init__(self, pos, dir, name):
        self.bod = [pos] #Lists [[x,y], [x,y]...]
        self.dir = dir #String 'direction'
        self.pos = pos.copy() #List [x,y]
        self.name = name #Name 'Chris'
        self.length = 1
        self.alive = True
        self.color = (randint(0,255),randint(0,255),randint(0,255))
    def getInfo(self):
        return [self.bod.copy(), self.dir, self.pos.copy()]
    def setDir(self, info):
        self.dir = getattr(playerUpdates, self.name)(self.pos.copy(), self.bod.copy(), self.dir, info.copy())
    def update(self, win):
        if self.alive:
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
            if len(self.bod) > length: #length is global, self.length is the class variable
                self.bod.pop(0)
        if self.alive:
            for i in self.bod:
                pygame.draw.rect(win, self.color, pygame.Rect(i[0], i[1], size, size))
            nameText = font.render(self.name, True, (100,100,100))
            loc = nameText.get_rect()
            loc.center = (self.pos[0]+10, self.pos[1]-14)
            w, h = loc.size
            pygame.draw.rect(win, (255,255,255), pygame.Rect(loc.x, loc.y, w, h))
            win.blit(nameText, loc)
        else:
            self.bod = []
            self.pos =[-100,-100]

def main():
    global length
    players = ['Chris', 'Person', 'Other']
    snakeList = []
    info = []
    tickRate = 5

    dirs = ['right', 'left', 'up', 'down']
    for i in players:
        snake = Snake([randint(0,(width/size)-1)*size, randint(0,(height/size)-1)*size], dirs[randint(0,3)], i)
        snakeList.append(snake)

    end = True
    playing = True
    tStart = time.time()
    while playing:
        clock.tick(tickRate)
        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
                end = False

        info = []
        for i in snakeList:
            info.append(i.getInfo())
        for i in snakeList:
            i.setDir(info.copy())
        #Check hit
        for i in snakeList:
            if i.alive:
                loc = i.getInfo()[2]
                for x in info:
                    if loc in x[0]:
                        if loc==x[0][-1]: #Checks if it is itself
                            temp = x[0].copy()
                            temp.remove(loc)
                            if loc in temp: #Checks to see if the value is in the list twice
                                i.alive = False
                                print(i.name, 'is out (Hit itself)')
                        else: #Makes sure it isn't current position
                            i.alive = False
                            print(i.name, 'is out (Hit snake)')
                if loc[0] < 0 or loc[0]>=width or loc[1]<0 or loc[1]>=height:
                    i.alive = False
                    print(i.name, 'is out (Border)')

        if (time.time()-tStart) > 1:
            length += 1
            tStart = time.time()
        if length > 3:
            tickRate = 40

        #Draw everything
        pygame.draw.rect(win, (0,0,0), pygame.Rect(0,0,width,height))
        for i in snakeList:
            i.update(win)
        pygame.draw.rect(win, (255,255,255), pygame.Rect(0,0,width,height), 1) #White border
        pygame.display.update()

    while end: #This is just so it doesn't immediately close after someone loses
        clock.tick(tickRate)
        for event in pygame.event.get():
            if event.type == QUIT:
                end = False
        keys = pygame.key.get_pressed()
        for i in keys:
            if i:
                end = False
        #Draw everything
        pygame.draw.rect(win, (0,0,0), pygame.Rect(0,0,width,height)) #Background


        pygame.display.update()
    pygame.quit()

class playerUpdates:
    #pos is [x,y] bod is [[x,y],[x,y]...]
    #info is [[bod, dir, pos], [bod, dir, pos]...]
    def Chris(pos, bod, dir, info):
        def hit(dirr, info, bod, pos):
            newX, newY = pos[0], pos[1]
            if dirr == 'right':
                newX += size
            if dirr == 'left':
                newX -= size
            if dirr == 'up':
                newY -= size
            if dirr == 'down':
                newY += size
            if newX >= width or newX < 0 or newY >= height or newY < 0:
                return True
            for i in info:
                badX, badY = i[2][0], i[2][1]
                if i[1] == 'right':
                    badX += size
                if i[1] == 'left':
                    badX -= size
                if i[1] == 'up':
                    badY -= size
                if i[1] == 'down':
                    badY += size

                if [newX, newY] in i[0]:
                        return True
                if [newX, newY] == [badX, badY]:
                    if bod == i[0]:
                        pass
                    else:
                        return True
            return False
        if not(hit(dir, info, bod, pos)) and not(randint(0,20)==1):
            return dir
        else:
            dirs = ['right', 'left', 'up', 'down']
            for i in range(0,4):
                newDir = dirs.pop(randint(0,len(dirs)-1))
                if not(hit(newDir, info, bod, pos)):
                    return newDir
            return dir
        return dir
    def Person(pos, bod, dir, info):
        def hit(dirr, info, bod, pos):
            if randint(0,20) == 1:
                return True
            newX, newY = pos[0], pos[1]
            if dirr == 'right':
                newX += size
            if dirr == 'left':
                newX -= size
            if dirr == 'up':
                newY -= size
            if dirr == 'down':
                newY += size
            if newX >= width or newX < 0 or newY >= height or newY < 0:
                return True
            for i in info:
                badX, badY = i[2][0], i[2][1]
                if i[1] == 'right':
                    badX += size
                if i[1] == 'left':
                    badX -= size
                if i[1] == 'up':
                    badY -= size
                if i[1] == 'down':
                    badY += size

                if [newX, newY] in i[0]:
                        return True
                if [newX, newY] == [badX, badY]:
                    if bod == i[0]:
                        pass
                    else:
                        return True
            return False
        if not(hit(dir, info, bod, pos)):
            return dir
        else:
            dirs = ['right', 'left', 'up', 'down']
            for i in range(0,4):
                newDir = dirs.pop(randint(0,len(dirs)-1))
                if not(hit(newDir, info, bod, pos)):
                    return newDir
            return dir

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
    def Other(pos, bod, dir, info):
        def hit(dirr, info, bod, pos):
            if randint(0,20) == 1:
                return True
            newX, newY = pos[0], pos[1]
            if dirr == 'right':
                newX += size
            if dirr == 'left':
                newX -= size
            if dirr == 'up':
                newY -= size
            if dirr == 'down':
                newY += size
            if newX >= width or newX < 0 or newY >= height or newY < 0:
                return True
            for i in info:
                badX, badY = i[2][0], i[2][1]
                if i[1] == 'right':
                    badX += size
                if i[1] == 'left':
                    badX -= size
                if i[1] == 'up':
                    badY -= size
                if i[1] == 'down':
                    badY += size

                if [newX, newY] in i[0]:
                        return True
                if [newX, newY] == [badX, badY]:
                    if bod == i[0]:
                        pass
                    else:
                        return True
            return False
        if not(hit(dir, info, bod, pos)):
            return dir
        else:
            dirs = ['right', 'left', 'up', 'down']
            for i in range(0,4):
                newDir = dirs.pop(randint(0,len(dirs)-1))
                if not(hit(newDir, info, bod, pos)):
                    return newDir
            return dir

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
