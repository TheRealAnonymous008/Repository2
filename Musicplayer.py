import os

try:
    import numpy
    if numpy.__version__ != "1.19.3":
        os.system("pip install numpy==1.19.3")
except:
    os.system("pip install numpy==1.19.3")

try:
    import pygame
except:
    os.system("pip install pygame")

try: 
    import scipy.io
except:
    os.system("pip install scipy")

try:
    import pydub
except:
    os.system("pip install pydub")

for file in os.listdir("."):
    print(file)
    if file == "DFT.py":
        os.system("DFT.py")
        break