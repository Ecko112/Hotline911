import pygame
import os

pygame.font.init()

NOTRUFDir = os.path.dirname(os.path.abspath(__file__))
IMAGESDir = os.path.join(NOTRUFDir, 'IMAGES')

X = 0
Y = 1


class Scba:

    def __init__(self):
        self.Bodyguard = Bodyguard()

class Bodyguard:

    def __init__(self):
        self.image = pass
