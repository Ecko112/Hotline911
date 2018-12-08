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
        self.spray = 60
        self.debit = 100
        self.min_spray = 10
        self.middle_spray = 0
        self.max_spray = 160
        self.min_debit = 25
        self.max_debit = 250
        # SELF
        self.sprayed = False
        self.hose_p = (int(self.handler.pos[X] + UNIT.SIZE * math.cos(self.handler.orientation)), int(self.handler.pos[Y] + self.handler.SIZE * math.sin(self.handler.orientation)))

    def spray_water(self, unit):
        self.handler = unit
        self.hose_p = (int(self.handler.pos[X]+unit.SIZE*math.cos(self.handler.orientation*(math.pi/180))), int(self.handler.pos[Y]+self.handler.SIZE*math.sin(self.handler.orientation*(math.pi/180))))
        unit.spraying = True
        if len(self.LEVEL.Water) < 500:
            self.spray_actual_water()
        else:
            # [DEV] UNLIMITED WATER PARICLES
            #     self.spray_actual_water()
            pass

    def spray_actual_water(self):
        nbr_water_entities = int(self.spray/3)
        # nbr_water_entities = 3
        direction = self.handler.orientation - self.spray/2
        for water in range(0, nbr_water_entities+1, 1):
            # direction += self.spray/nbr_water_entities
            direction += self.spray/nbr_water_entities
            alpha = direction - self.handler.orientation
            max_dist = self.debit*math.cos(alpha*(math.pi/180))
            class_water.Water(self, direction, max_dist, self.LEVEL)

    def set_hose_spray(self, sens):
        self.spray += 5 * sens
        if self.spray < self.min_spray:
            self.spray = self.min_spray
        elif self.spray > self.max_spray:
            self.spray = self.max_spray

    def set_hose_debit(self, sens):
        self.debit += 5 * sens
        if self.debit < self.min_debit:
            self.debit = self.min_debit
        elif self.debit > self.max_debit:
            self.debit = self.max_debit
