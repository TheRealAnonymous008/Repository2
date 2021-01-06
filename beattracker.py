import pygame
import sys

SWIDTH = 800
SHEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class Beat:
    def __init__(self, time):
        self.time = time

    def display(self):
        print("Beat registered at " + str(self.time) + "ms")

    def getData(self):
        return str(self.time)

class BeatMap:
    def __init__(self):
        self.beats = []

    def addBeat(self, time):
        self.beats.append(Beat(time))

    def display(self):
        for beat in self.beats:
            beat.display()
    
    def peek(self):
        if len(self.beats) == 0:
            return None

        return self.beats[0]

    def pop(self):
        if len(self.beats) == 0:
            return
        self.beats.pop(0)

    def adjust(self):
        root = self.beats[0].time
        for b in self.beats:
            b.time -= root


def getBeatMap():
    beatmap = BeatMap()
    screen = initializeScreen()
    color = BLACK
    playing = True

    font = loadFont()
    currTime = 0
    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])
    center = (SWIDTH / 3, SHEIGHT / 2)

    while playing:
        currTime = pygame.time.get_ticks()
        for e in pygame.event.get():
            color = BLACK

            if e.type == pygame.QUIT:
                playing = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                beatmap.addBeat(currTime)
                color = WHITE

        screen.fill(color)
        displayTextOnScreen(screen, font, (0, 30), str(currTime))
        displayTextOnScreen(screen, font, center, str("Tap to the beat"))
        pygame.display.flip()

    return beatmap

def initializeScreen():
    screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
    pygame.init()
    return screen

def loadFont():
    font = pygame.font.SysFont('Cambria Math', 30)
    return font

def displayTextOnScreen(screen, font, location, text):
    textSurface = font.render(text, False, GREEN)
    screen.blit(textSurface, location)

def writeBeatMapToFile(beatmap, filename = ""):
    try:
        f = open(filename +".txt", "w")
        for beat in beatmap.beats:
            f.write(str(beat.getData()) + "\n")

        f.close()
    except(FileNotFoundError):
        print("Not found error")