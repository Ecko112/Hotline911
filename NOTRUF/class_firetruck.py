from NOTRUF import class_hose
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
        self.hose = None
        # SET
        self.length = int(self.SCREEN_RESOLUTION[X]//5)
        self.width = int(self.SCREEN_RESOLUTION[X]//10)
        self.pos = [0, self.SCREEN_RESOLUTION[Y]-self.width]
        # TOOLS
        # Hose
        self.hose_pos = None
        self.tool_up()
        # Save
        self.LEVEL.Vehicles.append(self)

    def tool_up(self):
        self.hose_pos = [self.pos[X]+2*self.length//10, self.pos[Y]]
        self.hose = class_hose.Hose(self)

    def paint_truck(self):
        pygame.draw.rect(self.SCREEN, (255, 10, 20), (self.pos, (self.length, self.width)))
        pygame.draw.circle(self.SCREEN, (0, 0, 0), self.hose_pos, self.length//30)

    def arrival(self):
        if self.pos[X] < self.SCREEN_RESOLUTION[X] - self.length*2:
            self.pos[X] += self.SCREEN_RESOLUTION[X]//1366
            self.hose_pos[X] += self.SCREEN_RESOLUTION[X]//1366
        else:
            self.LEVEL.intro_is_done = True
