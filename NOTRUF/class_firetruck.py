from NOTRUF import class_hose, class_scba
import pygame

X = 0
Y = 1


class Truck:
    def __init__(self, LEVEL):
        # INIT
        self.LEVEL = LEVEL
        self.MAIN = self.LEVEL.MAIN
        self.SCREEN = self.LEVEL.SCREEN
        self.SCREEN_RESOLUTION = self.LEVEL.SCREEN_RESOLUTION
        # SET
        self.length = int(self.SCREEN_RESOLUTION[X]//5)
        self.width = int(self.SCREEN_RESOLUTION[X]//10)
        self.pos = [0, self.SCREEN_RESOLUTION[Y]-self.width]
        # TOOLS
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
        self.hose_pos = [self.pos[X]+2*self.length//10, self.pos[Y]]
        self.hose = class_hose.Hose(self)
        # Scba
        self.scba_pos = [self.pos[X]+4*self.length//10, self.pos[Y]]

    def paint_truck(self):
        pygame.draw.rect(self.SCREEN, (255, 10, 20), (self.pos, (self.length, self.width)))
        pygame.draw.circle(self.SCREEN, (0, 0, 0), self.hose_pos, self.length//30)

    def arrival(self):
        if self.pos[X] < 6*self.SCREEN_RESOLUTION[X]//10:
            self.pos[X] += self.SCREEN_RESOLUTION[X]//1366
            self.hose_pos[X] += self.SCREEN_RESOLUTION[X]//1366
        else:
            self.LEVEL.intro_is_done = True
            self.tool_up()
