# import pygame
import math
from NOTRUF import class_water

X = 0
Y = 1


class Hose:

    def __init__(self, unit):
        self.spray = math.pi / 20
        self.debit = 100
        self.water = []
        self.min_spray = math.pi / 30
        self.max_spray = 8 * math.pi / 20
        self.min_debit = 25
        self.max_debit = 250
        # SELF
        self.handler = unit
        self.sprayed = False
        self.hose_p = (int(self.handler.pos[X]+unit.SIZE*math.cos(self.handler.orientation)), int(self.handler.pos[Y]+self.handler.SIZE*math.sin(self.handler.orientation)))

    def spray_water(self, unit):
        self.handler = unit
        self.hose_p = (int(self.handler.pos[X]+unit.SIZE*math.cos(self.handler.orientation)), int(self.handler.pos[Y]+self.handler.SIZE*math.sin(self.handler.orientation)))
        unit.spraying = True
        if len(self.water) < 500:
            self.spray_actual_water()
        else:
            # [DEV] UNLIMITED WATER PARICLES
            #     self.spray_actual_water()
            pass

    def spray_actual_water(self):
        nbr_water_entities = int(self.spray*50)
        direction = self.handler.orientation - self.spray/2 -(self.spray*2/nbr_water_entities)
        for water in range(0, nbr_water_entities+1, 1):
            direction += self.spray/nbr_water_entities
            class_water.Water(self, direction)

    def set_hose_spray(self, sens):
        self.spray += (math.pi/100) * sens
        if self.spray < self.min_spray:
            self.spray = self.min_spray
        elif self.spray > self.max_spray:
            self.spray = self.max_spray

    def set_hose_debit(self, sens):
        self.debit += 10 * sens
        if self.debit < self.min_debit:
            self.debit = self.min_debit
        elif self.debit > self.max_debit:
            self.debit = self.max_debit

    def move_water(self):
        for water in self.water:
            water.mov_water()
