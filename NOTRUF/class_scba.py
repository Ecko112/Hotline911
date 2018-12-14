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
        self.capacity = 300
        self.temp = 'N/A'
        self.pos = [self.TRUCK.scba_pos[X], self.TRUCK.scba_pos[Y]-10]
        self.bodyguard = Bodyguard(self)
        self.handler = None
        self.LEVEL.Tools.append(self)

    def paint_scba(self):
        if self.handler is None:
            # Blit SCBA item
            self.SCREEN.blit(self.image, (self.pos[X]-self.scale_up//2, self.pos[Y]-self.scale_up//2))
        elif self.handler.checking:
            # Blit Bodyguard
            self.bodyguard.paint_bodyguard()

    def get_picked_up(self, unit):
        self.handler = unit
        self.handler.scba = self

    def get_dropped(self):
        self.pos = self.handler.pos
        self.handler = None


class Bodyguard:

    def __init__(self, SCBA):
        # INIT
        self.SCBA = SCBA
        self.SCREEN = self.SCBA.SCREEN
        self.SCREEN_RESOLUTION = self.SCBA.SCREEN_RESOLUTION
        # Image
        self.scale_up = [int(self.SCREEN_RESOLUTION[X]//14.23), int(self.SCREEN_RESOLUTION[X]//5.69)]
        self.image = pygame.image.load(IMAGESDir+'/tool_bodyguard.png')
        self.image = pygame.transform.scale(self.image, self.scale_up)
        self.pos = [9*self.SCREEN_RESOLUTION[X]//10, 1*self.SCREEN_RESOLUTION[Y]//10]
        # Display Air Capacity
        self.capacity_message_font_size = int(self.SCREEN_RESOLUTION[X]//60)
        self.capacity_message_font = pygame.font.SysFont('monospace', self.capacity_message_font_size)
        self.capacity_message = self.capacity_message_font.render(str(int(self.SCBA.capacity)), True, (0, 0, 0))
        # Display Room Temp
        self.temp_message_font_size = self.capacity_message_font_size
        self.temp_message_font = self.capacity_message_font
        self.temp_message = self.temp_message_font.render(self.SCBA.temp, True, (0, 0, 0))

    def paint_bodyguard(self):
        # Blit bodyguard
        self.SCREEN.blit(self.image, self.pos)
        # Update stats
        self.temp_message = self.temp_message_font.render(self.SCBA.temp, True, (0, 0, 0))
        self.capacity_message = self.capacity_message_font.render(str(int(self.SCBA.capacity)), True, (0, 0, 0))
        # Blit stats
        self.SCREEN.blit(self.capacity_message, (self.pos[X]+self.SCREEN_RESOLUTION[X]//50.59, self.pos[Y]+self.SCREEN_RESOLUTION[X]//50.59))
        self.SCREEN.blit(self.temp_message, ((self.pos[X]+10), self.pos[Y]+self.SCREEN_RESOLUTION[X]//50.59+15))
