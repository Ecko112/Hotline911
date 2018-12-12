import pygame
import os

pygame.font.init()

NOTRUFDir = os.path.dirname(os.path.abspath(__file__))
IMAGESDir = os.path.join(NOTRUFDir, 'IMAGES')

X = 0
Y = 1


class Scba:

    def __init__(self, TRUCK):
        # INIT
        self.TRUCK = TRUCK
        self.LEVEL = self.TRUCK.LEVEL
        self.MAIN = self.TRUCK.MAIN
        self.SCREEN = self.TRUCK.SCREEN
        self.SCREEN_RESOLUTION = self.TRUCK.SCREEN_RESOLUTION
        # Image
        self.image = pygame.Rect(0, 0, 10, 20)
        # SELF
        self.pos = [self.TRUCK.scba_pos[X], self.TRUCK.scba_pos[Y]-10]
        self.Rect = pygame.Rect(0, 0, self.TRUCK.length//20, self.TRUCK.length//20)
        self.Rect.center = self.pos
        self.handler = None
        self.texture = (10, 10, 10)
        self.capacity = 300
        self.LEVEL.Tools.append(self)

    def paint_scba(self):
        if self.handler is None:
            self.Rect.center = self.pos
            pygame.draw.rect(self.SCREEN, self.texture, self.Rect)

    def get_picked_up(self, unit):
        self.handler = unit
        self.handler.scba = self

    def get_dropped(self):
        self.pos = self.handler.pos
        self.handler = None


class Bodyguard:

    def __init__(self, SCBA):
        self.SCBA = SCBA
        self.image = pygame.Rect()
