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
        self.scale_up = int(self.LEVEL.PLAYER_SIZE*2.75)
        self.image = pygame.image.load(IMAGESDir+'/tool_scba.png').convert_alpha(self.SCREEN)
        self.image = pygame.transform.scale(self.image, (self.scale_up, self.scale_up))
        # SELF
        self.pos = [self.TRUCK.scba_pos[X], self.TRUCK.scba_pos[Y]-10]
        self.bodyguard = Bodyguard(self)
        self.handler = None
        self.texture = (10, 10, 10)
        self.capacity = 300
        self.LEVEL.Tools.append(self)

    def paint_scba(self):
        if self.handler is None:
            self.SCREEN.blit(self.image, (self.pos[X]-self.scale_up//2, self.pos[Y]-self.scale_up//2))
        elif self.handler.checking:
            self.bodyguard.paint_bodyguard()

    def get_picked_up(self, unit):
        self.handler = unit
        self.handler.scba = self

    def get_dropped(self):
        self.pos = self.handler.pos
        self.handler = None


class Bodyguard:

    def __init__(self, SCBA):
        self.SCBA = SCBA
        self.SCREEN = self.SCBA.SCREEN
        self.image = pygame.image.load(IMAGESDir+'/tool_bodyguard.png')

    def paint_bodyguard(self):
        self.SCREEN.blit(self.image, (0, 0))
