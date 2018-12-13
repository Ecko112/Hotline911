import pygame
import math
import os
import class_water

NOTRUFDir = os.path.dirname(os.path.abspath(__file__))
IMAGESDir = os.path.join(NOTRUFDir, 'IMAGES')

X = 0
Y = 1


class Hose:

    def __init__(self, TRUCK):
        # INIT
        self.TRUCK = TRUCK
        self.LEVEL = self.TRUCK.LEVEL
        self.MAIN = self.TRUCK.MAIN
        self.SCREEN = self.TRUCK.SCREEN
        self.pos = self.TRUCK.hose_pos
        # Image
        self.scale_up = int(self.LEVEL.SCREEN_RESOLUTION[X] // 56.91)
        self.image = pygame.image.load(IMAGESDir+'/tool_hose.png').convert_alpha(self.SCREEN)
        self.image = pygame.transform.scale(self.image, (self.scale_up, self.scale_up))
        # Spray Settings
        min_spray = 10
        medium_spray = 60
        max_spray = 150
        self.spray_presets = [min_spray, medium_spray, max_spray]
        self.spray = self.spray_presets[0]
        # Debit Settings
        self.min_debit = 100
        self.max_debit = 350
        self.debit = 180
        # SELF
        self.handler = None
        self.hose_p = None
        self.sprayed = False
        self.hose_line = [self.pos, self.pos, self.pos]
        self.texture = (206, 5, 5)
        self.LEVEL.Tools.append(self)

    def paint_hose(self):
        pygame.draw.lines(self.SCREEN, self.texture, False, self.hose_line, 10)
        if self.handler is not None:
            self.set_hose_line()
        else:
            self.SCREEN.blit(self.image, (self.pos[X] - self.scale_up // 2, self.pos[Y] - self.scale_up // 2))

    def get_picked_up(self, unit):
        self.handler = unit
        self.handler.hose = self

    def get_dropped(self):
        if get_dist(self.handler.pos, self.TRUCK.hose_pos) < 35:
            self.pos = self.TRUCK.hose_pos
            self.hose_line = [self.pos, self.pos, self.pos]
            self.handler = None
        else:
            self.pos = self.handler.pos
            self.handler = None

    def set_hose_line(self):
        self.hose_line[-1] = self.handler.pos
        dist = get_dist(self.handler.pos, self.hose_line[-2])
        if dist > 75:
            self.hose_line.insert(-1, self.handler.pos[:])
        elif len(self.hose_line) > 3:
            if get_dist(self.handler.pos, self.hose_line[-3]) < 100:
                self.hose_line.pop(-2)
        elif len(self.hose_line) == 2:
            if get_dist(self.hose_line[0], self.hose_line[1]) < 100:
                self.hose_line.pop(-1)
                self.hose_line.append(self.handler.pos)

    def spray_water(self):
        self.handler.spraying = True
        if len(self.LEVEL.Water) < 500:
            self.spray_actual_water()
        else:
            # [DEV] UNLIMITED WATER PARICLES
            # self.spray_actual_water()
            pass

    def spray_actual_water(self):
        self.hose_p = (int(self.handler.pos[X]+self.handler.SIZE*math.cos(self.handler.orientation*(math.pi/180))), int(self.handler.pos[Y]+self.handler.SIZE*math.sin(self.handler.orientation*(math.pi/180))))
        nbr_water_entities = int(self.spray/3)
        direction = self.handler.orientation - self.spray/2
        for water in range(0, nbr_water_entities+1, 1):
            direction += self.spray/nbr_water_entities
            alpha = direction - self.handler.orientation
            max_dist = self.debit / math.cos(alpha * (math.pi / 180))
            if self.spray == self.spray_presets[2]:
                max_dist /= 8
            elif self.spray == self.spray_presets[1]:
                max_dist /= 2
            class_water.Water(self, direction, max_dist, self.LEVEL)

    def set_hose_spray(self, preset):
        self.spray = self.spray_presets[preset]

    def set_hose_debit(self, sens):
        self.debit += 5 * sens
        if self.debit < self.min_debit:
            self.debit = self.min_debit
        elif self.debit > self.max_debit:
            self.debit = self.max_debit


def get_dist(point1, point2):
    return int(math.sqrt(((point1[X]-point2[X])**2)+(point1[Y]-point2[Y])**2))


def get_angle(point1, point2):
    return math.atan2(point2[Y]-point1[Y], point2[X]-point1[X])
