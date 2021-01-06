import numpy as np
import random
import pygame
from scipy.io import wavfile
import scipy.io
import sys
import os
import math
from pydub import AudioSegment

# Set countdown here (in secs)
COUNTDOWN = 3
# Number of samples in DFT
FREQS = 2000

#Define the lowest frequency
LOWFREQ = 20
# Define the dimensions of the screen
SWIDTH = 1000
SHEIGHT = 800

RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define constants for play back and play forward (in secondss)
BACKTIME =5
FORTIME = 5

# Initialize pygame
pygame.init()

#For isolating channels
LCHANNEL = True
RCHANNEL = False

FACTPOWER = 1

# For windowing function
BETA  = 10

#initialize factors
FACTS = []
def initializeFactors():
    for i in range(0, FREQS):
        FACTS.append(math.pow(i, FACTPOWER))

# Initialize the location of ffmpeg


def locateFFMPEG(currpath):
    for file in os.listdir(currpath):
        print(file)
        if(file == "ffmpeg.exe"):
            return os.path.abspath(file)

AudioSegment.converter = locateFFMPEG(".")


# Load fonts
pygame.font.init()

font = pygame.font.SysFont('Cambria Math', 30)
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))

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

def processFile(file):
    if file.endswith(".wav"):
        return file
    elif file.endswith(".mp3"):
        sound = AudioSegment.from_mp3(file)
        sound.export(file.removesuffix(".mp3") + ".wav", format="wav")
        return file.removesuffix(".mp3") + ".wav"

    return ""


def scale(arr):
    # THe following function scales the elements of an array to be of the range (0, 800)
    if(len(arr) == 0):
        return arr

    maximum = max(SHEIGHT / 2, max(arr))
    minimum = min(-SHEIGHT / 2, min(arr))

    # Scale the array such that maximum is screen height and minimum is 0
    res = []
    if(maximum == minimum):
        return [0 for i in range(0, len(arr))]
    for element in arr:
        if element == 0:
            res.append(0)
        else:
            res.append(((element) / (maximum - minimum)) * SHEIGHT / 2)

    return res
        

def drawFreqs(res, color):
    # Perform scaling so frequencies can fit on screen
    res = scale(res)
    
    # Draw frequencies
    for i in range(0, len(res)):
        if(res[i] > 0 ):
            pygame.draw.rect(screen, color, (2 * i * SWIDTH / FREQS, 
                                                    SHEIGHT/2  - res[i], 
                                                    2 * SWIDTH / FREQS, res[i] ))
        else: 
            pygame.draw.rect(screen, color, (2 * i * SWIDTH / FREQS, 
                                                    SHEIGHT / 2, 
                                                    2 * SWIDTH / FREQS, -res[i] ))
    
    
def drawTimer(time):
    # Display the time on screen
    timeSurface = font.render(str(int(time)) + "s", False, (0, 255, 0))
    screen.blit(timeSurface, (SWIDTH / 2,30))

def drawBar(curr, data):
    # Draw the loading bar
    pygame.draw.rect(screen, (255, 255, 255), (0,10, SWIDTH * (curr / data),10))

def DFT(sequence):
    
    win = np.kaiser(len(sequence), BETA)
    # The following function performs a discrete fourier transform and returns an array of magnitudes
    dft = np.fft.rfft(sequence * win, FREQS)
    res =[]
    # Calculate magnitude of each component
    # Note we omit frequencies below the LOWFREQ. This is so we can only focus on a band on the spectrum.
    # It is also recommended to omit the value associated with 0 Hz as this heavily skews the spectrum.
    for i in range(LOWFREQ, len(dft)):
        # Multiply by a factor proportional to the frequency.
        # This is similar to a discrete wavelet transform, which is time dependent. Low frequencies last longer .
        res.append(dft[i].real * FACTS[i])
    return res

def printLabel(label):
    textsurface = font.render(label, False, (0, 255, 0))
    screen.blit(textsurface, (SWIDTH / 2,SHEIGHT-30))

def performCountdown(start, filepath):
    while (pygame.time.get_ticks()/1000 - start < COUNTDOWN):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                os.remove(filepath)
                sys.exit()
        screen.fill((0, 0, 0))
        drawTimer(4 - pygame.time.get_ticks() / 1000 + start)
        pygame.display.flip()


def main():

    # Make sure ffmpeg is in the directory
    if AudioSegment.converter == None:
        print("Warning, ffmpeg was not located")
        return

    # Locate a file to process
    filetoprocess = locateFile()
    filepath = processFile(filetoprocess)

    # Initialize a mixer
    pygame.mixer.init()

    #initialize squares
    initializeFactors()

    # Check if filepath actually exists
    if not filepath.endswith(".wav"):
        print("Warning. No Wav File detected. Program Terminated")
        return
        
    samplerate, data = wavfile.read(filepath)

    # Get left and right channels
    dat = data[:, 0]
    rdat = data[:,1]
    # Store current position in the sequence
    curr = 0 

    # Flags for controlling pausing and playing
    playing = False
    trackPlayed = False
    
    # start is an accumulator determining the last processed time value
    start = pygame.time.get_ticks()
    UPDATE = pygame.USEREVENT + 1
    clock = pygame.time.Clock()
    dt = 0
    # Duration controls the duration of the track
    duration = len(data) / samplerate

    # Currenttime determines the current time in the track
    currentTime = 0
    clock.tick(60)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # When done, delete the wav file if the original was an mp3
                os.remove(filepath)
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    # Left arrow corresponds to play back
                    curr = max(0, curr - BACKTIME * samplerate)
                    currentTime = max(0, currentTime - BACKTIME)
                    pygame.mixer.music.play(start = currentTime)
                    if not playing:
                        pygame.mixer.music.pause()

                if e.key == pygame.K_RIGHT:
                    # Right Arrow corresponds to play forward
                    curr = min(len(data), curr + FORTIME * samplerate)
                    currentTime = min(duration, currentTime + FORTIME)
                    pygame.mixer.music.play(start = currentTime)
                    if not playing:
                        pygame.mixer.music.pause()

                if e.key == pygame.K_SPACE:
                    # SPACE pauses and plays a file
                    # Make sure the file is actually there:
                    if not filepath.endswith(".wav"):
                        screen.fill((0, 0, 0))
                        printLabel("Error: No wavFile Detected")
                        pygame.display.flip()
                        break

                    start = pygame.time.get_ticks() / 1000
                    # Perform a countdown here at the start
                    if not playing and not trackPlayed:
                        performCountdown(start, filepath)

                    # Reset start back to the current time
                    start = pygame.time.get_ticks() / 1000


                    # Handle pausing and playing here
                    playing = not playing
                    if not trackPlayed:
                        pygame.mixer.music.load(filetoprocess)
                        pygame.mixer.music.play()
                        trackPlayed = not trackPlayed 

                    if playing:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()

                    pygame.time.set_timer(UPDATE, 20)

            if e.type == UPDATE:
                if trackPlayed:
                    # dt is time elapsed (in seconds)
                    
                    screen.fill((0, 0, 0))
                    
                    if playing:
                        dt = (pygame.time.get_ticks() / 1000) - start 
                        start = pygame.time.get_ticks() / 1000
                        

                        # Get the number of samples to be sampled here
                        smp = int(samplerate * dt)
                        # Get sequence here
                        sequence = []
                        rsequence = []

                        
                        for i in range(0, smp):
                            # Stop when the end of the list is reached
                            if curr + i >= len(data):
                                break
                            elif curr + i < 0:
                                continue
                            sequence.append(dat[curr + i])
                            rsequence.append(rdat[curr + i])

                        

                        curr += smp
                        # Update currentTime
                        currentTime += dt
                        if LCHANNEL:
                        # Perform DFT
                            res = DFT(sequence)
                            drawFreqs(res, RED)
                        if RCHANNEL:
                        # Perform DFT on other side
                            dres = DFT(rsequence)
                            drawFreqs(dres, BLUE)
    
                    drawTimer(currentTime - 1)
                    drawBar(curr, len(dat))
                    printLabel("Now playing " + filepath)
                    pygame.display.flip()
    
    

main()

input("Press any key to continue")

