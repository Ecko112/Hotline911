import class_hose, class_scba, class_level
import pygame
import os

NOTRUFDir = os.path.dirname(os.path.abspath(__file__))
IMAGESDir = os.path.join(NOTRUFDir, 'IMAGES')

X = 0
Y = 1


class Truck:
    def __init__(self, LEVEL):
        # INIT
        self.LEVEL = LEVEL
        self.MAIN = self.LEVEL.MAIN
        self.SCREEN = self.LEVEL.SCREEN
        self.SCREEN_RESOLUTION = self.LEVEL.SCREEN_RESOLUTION
        # Image
        self.scale_up = [int(self.SCREEN_RESOLUTION[X]//5.83*1.5), int(self.SCREEN_RESOLUTION[X]//12.19*1.5)]
        self.image = pygame.image.load(IMAGESDir+'/truck_engine.png').convert_alpha(self.SCREEN)
        self.image = pygame.transform.scale(self.image, self.scale_up)
        self.pos = [-self.SCREEN_RESOLUTION[Y]//2, 98*self.SCREEN_RESOLUTION[Y]//100-self.scale_up[Y]]
        # TOOLS
        self.door = pygame.Rect(0, 0, self.scale_up[X] // 4, self.scale_up[X] // 4)
        # Hose
        self.hose = None
        self.hose_pos = None
        # Scba
        self.scba = None
        self.scba_pos = None
        # Save
        self.LEVEL.Vehicles.append(self)

    def tool_up(self):
        # Hose
        self.hose_pos = [self.pos[X]+2*self.scale_up[X]//10, self.pos[Y]]
        self.hose = class_hose.Hose(self)
        # Scba
        self.scba_pos = [self.pos[X]+4*self.scale_up[X]//10, self.pos[Y]]
        self.scba = class_scba.Scba(self)

    def paint_truck(self):
        self.SCREEN.blit(self.image, self.pos)
        if self.LEVEL.__class__ is class_level.Level:
            if self.LEVEL.intro_is_done:
                self.door.bottomright = [self.pos[X] + self.scale_up[X], self.pos[Y]]
        else:
            self.door.bottomleft = [self.pos[X]+self.scale_up[Y], self.pos[Y]+self.scale_up[X]]

    def arrival(self):
        if self.pos[X] < 6*self.SCREEN_RESOLUTION[X]//10:
            self.pos[X] += self.SCREEN_RESOLUTION[X]/1366
        else:
            self.LEVEL.intro_is_done = True
            self.pos = [int(self.pos[X]), int(self.pos[Y])]
            self.tool_up()
