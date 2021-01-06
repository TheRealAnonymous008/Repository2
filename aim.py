# The following is an aim training program. Circles appear on the screen where the user can click on.
# Accuracy of clicks is measured.

from beattracker import *
import pygame
import sys
import random
import math
import os
from enum import Enum

FILENAME = "apple"          # No need to include the .txt

class Mode(Enum):
    default = 1         # All circles are randomly generated
    custom = 2          # All circles are read from the beat.txt file
    generate = 3        # All cirlces are written to the beat.txt file

MODE = Mode.custom

SWIDTH, SHEIGHT = 800, 800
CAPACITY = 20
BEAT = 400

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class CircleBiasManager:
    def __init__(self):
        self.aimCircleBias = 0.5
        self.movementBias = 0.5

class CircleConstantManager:
    def __init__(self):
        self.life = 500           
        self.spawnDelay = 0
        self.rad = 75
        self.radRate = 25 / 1000 

class Timer:
    def __init__(self):
        self.curr = 0               # in ms
        self.deltaTime = 0          # in ms
        self.beat = BEAT             # in ms

    def changeBeat(self, beat):
        self.beat = beat
        self.curr = pygame.time.get_ticks()
        self.deltaTime = 0

    def registerBeat(self):
        t = pygame.time.get_ticks()
        self.deltaTime = t - self.curr

        if self.deltaTime >= self.beat:
            self.curr = t
            self.deltaTime = 0
            return True
        
        return False

class GenericObject:
    def __init__(self):
        pass

    def update(self):
        pass

    def drawOnScreen(self, screen):
        pass

    def onMouseClick(self):
        pass

    def checkIfClicked(self, mousex, mousey):
        pass

    def checkIfDead(self):
        pass

    def calculateScore(self, mousex, mousey):
        pass

class Circle(GenericObject):
    def __init__(self, xpos, ypos, rad, rate):
        super().__init__()
        self.xpos = xpos
        self.ypos = ypos
        self.rad = rad
        self.shrinkRate = rate

    def drawOnScreen(self, screen):
        pygame.draw.circle(screen, WHITE, (self.xpos, self.ypos), int(self.rad))
        pygame.draw.circle(screen, RED, (self.xpos, self.ypos), int(self.rad / 4))

    def update(self):
        if self.rad > 0: 
            self.rad -= self.shrinkRate
        self.rad = max(self.rad, 0)

    def checkIfClicked(self, mousex, mousey):
        dx = mousex - self.xpos
        dy = mousey - self.ypos
        clickSquaredDistanceFromCenter = dx * dx + dy * dy

        if(clickSquaredDistanceFromCenter <= self.rad * self.rad):
            return True
        return False

    def checkIfDead(self):
        if self.rad <= 0:
            return True
        return False

    def calculateScore(self, mousex, mousey):
        dx = mousex - self.xpos
        dy = mousey - self.ypos
        c = math.sqrt(dx * dx + dy * dy)

        return int( float(1 - c / self.rad) * 100)

class FixedCircle(Circle):
    def __init__ (self, xpos, ypos, rad, rate, life, time):
        super().__init__(xpos, ypos, rad, rate)
        self.life = life
        self.birth = time
        self.time = None

    def update(self):
        self.time = pygame.time.get_ticks()

    def drawOnScreen(self, screen):
        comp = max(255 * self.getRatio(), 0)
        color = (int(comp), int(comp), int(comp))
        colorin = (0, 0, int(comp))
        pygame.draw.circle(screen, color, (self.xpos, self.ypos), int(self.rad))
        pygame.draw.circle(screen, colorin, (self.xpos, self.ypos), int(self.rad / 4))

    def getRatio(self):
        if self.time == None:
            return 0.9

        return float(1 - (self.time - self.birth) / (self.life))

    def checkIfDead(self):
        if self.time == None:
            return False
        if self.time >= self.birth + self.life:
            return True
        return False

class Mover(GenericObject):
    def __init__(self, circle, vx, vy):
        super().__init__()
        self.vx = vx
        self.vy = vy
        self.circle = circle

    def update(self):
        self.circle.xpos += self.vx
        self.circle.ypos += self.vy
        self.circle.update()

    def checkIfClicked(self, mousex, mousey):
        return self.circle.checkIfClicked(mousex, mousey)

    def checkIfDead(self):
        return self.circle.checkIfDead()

    def drawOnScreen(self, screen):
        self.circle.drawOnScreen(screen)

    def calculateScore(self, mousex, mousey):
        return self.circle.calculateScore(mousex, mousey)



class CircleManager:
    def __init__(self, bounds, capacity):
        self.circles = []
        self.lb , self.rb, self.ub, self.db = bounds
        self.capacity = capacity
        self.biasManager = CircleBiasManager()
        self.const = CircleConstantManager()

    def spawnCircle(self):
        if len(self.circles) >= self.capacity:
            return

        r = random.random()
        c = None
        if r < self.biasManager.aimCircleBias:
            c = self.spawnAimCircle()
        else:
            c = self.spawnFixedCircle()

        c = self.configureMovement(c)

        self.circles.append(c)

    def configureMovement(self, circle):
        r = random.random()
        if r >= self.biasManager.movementBias:
            return circle
        vx = random.uniform(0.05, 0.25)
        if circle.xpos > (self.lb + self.rb) / 2:
            vx *= -1

        vy = random.uniform(0.05, 0.25)
        if circle.ypos > (self.ub + self.db) / 2:
            vy *= -1

        return Mover(circle, vx, vy)
        
    def spawnFixedCircle(self):
        x, y = self.generateRandomPoint()
        t = pygame.time.get_ticks()
        return FixedCircle(x, y, self.const.rad, 0, self.const.life, t)

    def spawnAimCircle(self):
        x, y =self.generateRandomPoint()
        return Circle(x, y, self.const.rad, self.const.radRate)
    
    def generateRandomPoint(self):
        x = random.randrange(self.lb, self.rb)
        y = random.randrange(self.ub, self.db)
        return x, y

    def updateCircles(self):
        for c in self.circles:
            if c.checkIfDead():
                self.circles.remove(c)
                del c
            else:
                c.update()

    def drawCircles(self, screen):
        for c in self.circles:
            c.drawOnScreen(screen)

    def checkClick(self, mousex, mousey):
        maxScore = -1
        minCirc = None
        for c in self.circles:
            if c.checkIfClicked(mousex, mousey):
                score = c.calculateScore(mousex, mousey)
                if minCirc == None:
                    maxScore = score
                    minCirc = c
                elif maxScore < score:
                    minDist = score
                    minCirc = c
        return minCirc

    def removeCircle(self, circle):
        try:
            self.circles.remove(circle)
            del circle
        except(ValueError):
            pass

def main():
    screen = loadScreen()
    executeGameLoop(screen, MODE)

def executeGameLoop(screen, mode):
    if mode == Mode.default:
        executeDefaultGameLoop(screen)
    elif mode == Mode.custom:
        executeCustomGameLoop(screen)
    elif mode == Mode.generate:
        executeWriteLoop()

def executeWriteLoop():
    playTrack()
    beatmap = getBeatMap()
    writeBeatMapToFile(beatmap, FILENAME)
    sys.exit()
    

def executeDefaultGameLoop(screen):
    bounds = (50, SWIDTH - 50 , 50, SHEIGHT - 50)
    font = loadFont()
    manager = CircleManager(bounds, CAPACITY)
    timer = Timer()
    currScore = 0
    clicks = 0

    isPaused = False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    isPaused = not isPaused
            if e.type == pygame.MOUSEBUTTONDOWN and not isPaused:
                clicks = clicks + 1
                mousex, mousey = pygame.mouse.get_pos()
                clicked = manager.checkClick(mousex, mousey)

                if clicked != None:
                    currScore += clicked.calculateScore(mousex, mousey)
                    manager.removeCircle(clicked)

        screen.fill(BLACK)
        if not isPaused:
            if timer.registerBeat():
                manager.spawnCircle()
            
            manager.updateCircles()

        manager.drawCircles(screen)
        displayTextOnScreen(screen, font , (SWIDTH / 4,30),  "Current Score: " + str(currScore) )

        ave = getAverage(currScore, clicks)
        displayTextOnScreen(screen, font,  (SWIDTH / 4,60),  "Accuracy: " + str(ave) + "%")

        pygame.display.flip()

def executeCustomGameLoop(screen):
    bounds = (50, SWIDTH - 50 , 50, SHEIGHT - 50)
    font = loadFont()
    manager = CircleManager(bounds, CAPACITY)
    timer = Timer()
    currScore = 0
    clicks = 0

    beatmap = initializeBeatMap(FILENAME)
    spawnDelay = manager.const.spawnDelay
    playTrack()

    while True:
        time = pygame.time.get_ticks()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                clicks = clicks + 1
                mousex, mousey = pygame.mouse.get_pos()
                clicked = manager.checkClick(mousex, mousey)

                if clicked != None:
                    currScore += clicked.calculateScore(mousex, mousey)
                    manager.removeCircle(clicked)

        screen.fill(BLACK)
        if beatmap.peek() != None:
            if beatmap.peek().time - spawnDelay <= time:
                beatmap.pop()
                manager.spawnCircle()
    
        manager.updateCircles()

        manager.drawCircles(screen)
        displayTextOnScreen(screen, font , (SWIDTH / 4,30),  "Current Score: " + str(currScore) )

        ave = getAverage(currScore, clicks)
        displayTextOnScreen(screen, font,  (SWIDTH / 4,60),  "Accuracy: " + str(ave) + "%")

        pygame.display.flip()

def initializeBeatMap(filename):
    beatmap = BeatMap()

    f = open(filename + ".txt", "r")

    lines = f.readlines()
    for line in lines:
        beatmap.addBeat(int(line))

    f.close()
    return beatmap

def loadScreen():
    pygame.init()
    screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
    return screen

def loadFont():
    font = pygame.font.SysFont('Cambria Math', 30)
    return font

def displayTextOnScreen(screen, font, location, text):
    textSurface = font.render(text, False, GREEN)
    screen.blit(textSurface, location)

def getAverage(sum, n):
    if n == 0:
        return 0
    return "{:.2f}".format(sum / n)

def playTrack():
    filePath = locateFile()

    if not filePath.endswith(".wav") and not filePath.endswith(".mp3"):
        return 
    
    pygame.mixer.init()
    pygame.mixer.music.load(filePath)
    pygame.mixer.music.play()

def locateFile():
    # The following locates a wav file in the current directory    
    filepath = "./"
    candidates = []
    # Look for a wav file
    for file in os.listdir("."):
        if file.endswith(".wav"):
            candidates.append(filepath + file)
        # Otherwise look for an mp3 file 
        elif file.endswith(".mp3"):
            # Convert from mp3 to wav
            candidates.append(filepath + file) 
            

    # If there are multiple files perform a random selection
    if len(candidates) != 0:
        return random.choice(candidates)
    # Otherwise return filepath
    return filepath

main()