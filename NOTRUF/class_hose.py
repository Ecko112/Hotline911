import pygame
import math
from NOTRUF import class_water

X = 0
Y = 1


class Hose:

    def __init__(self, UNIT):
        # INIT
        self.handler = UNIT
        self.LEVEL = self.handler.LEVEL
        self.MAIN = self.LEVEL.MAIN
        self.SCREEN = self.LEVEL.SCREEN
        self.pos = self.handler.pos
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
        self.sprayed = False
        self.hose_line = [self.handler.pos, self.handler.pos]
        self.texture = (206, 5, 5)
        self.LEVEL.Tools.append(self)

    def paint_hose(self):
        self.set_hose_line()
        pygame.draw.lines(self.SCREEN, self.texture, False, self.hose_line, 10)

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
        self.hose_p = (int(self.handler.pos[X]+self.handler.SIZE*math.cos(self.handler.orientation*(math.pi/180))), int(self.handler.pos[Y]+self.handler.SIZE*math.sin(self.handler.orientation*(math.pi/180))))
        self.handler.spraying = True
        if len(self.LEVEL.Water) < 500:
            self.spray_actual_water()
        else:
            # [DEV] UNLIMITED WATER PARICLES
            #     self.spray_actual_water()
            pass

    def spray_actual_water(self):
        nbr_water_entities = int(self.spray/3)
        direction = self.handler.orientation - self.spray/2
        for water in range(0, nbr_water_entities+1, 1):
            # direction += self.spray/nbr_water_entities
            direction += self.spray/nbr_water_entities
            alpha = direction - self.handler.orientation
            max_dist = self.debit / math.cos(alpha * (math.pi / 180))
            if self.spray == self.spray_presets[2]:
                max_dist /= 8
            elif self.spray == self.spray_presets[1]:
                max_dist /= 2
                pass

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


