import pygame
import math
from NOTRUF import class_water

X = 0
Y = 1


class Hose:
    spray = math.pi/20
    debit = 100
    water = []
    watercone = []
    waterfront_length = 0
    waterfront = None
    min_spray = math.pi/30
    max_spray = 8*math.pi/20
    min_debit = 25
    max_debit = 250
    # SELF
    handler = None
    sprayed = False

    def __init__(self):
        pass

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

    def set_hose_spray(self, input):
        self.spray += (math.pi/100)*input
        if self.spray < self.min_spray:
            self.spray = self.min_spray
        elif self.spray > self.max_spray:
            self.spray = self.max_spray

    def set_hose_debit(self, input):
        self.debit += 10*input
        if self.debit < self.min_debit:
            self.debit = self.min_debit
        elif self.debit > self.max_debit:
            self.debit = self.max_debit

    def move_water(self):
        for water in self.water:
            water.mov_water()
