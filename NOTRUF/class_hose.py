# import pygame
import math
from NOTRUF import class_water

X = 0
Y = 1


class Hose:

    def __init__(self, UNIT):
        self.handler = UNIT
        # INIT
        self.LEVEL = self.handler.LEVEL
        self.MAIN = self.LEVEL.MAIN
        # Spray Settings
        min_spray = 10
        medium_spray = 60
        max_spray = 160
        self.spray_presets = [min_spray, medium_spray, max_spray]
        self.spray = self.spray_presets[0]

        self.min_debit = 70
        self.max_debit = 350
        self.debit = 100

        # SELF
        self.sprayed = False
        self.hose_p = (int(self.handler.pos[X] + UNIT.SIZE * math.cos(self.handler.orientation)), int(self.handler.pos[Y] + self.handler.SIZE * math.sin(self.handler.orientation)))

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
            if self.spray > 60:
                max_dist /= 8
            else:
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
