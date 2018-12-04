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
    min_spray = math.pi/20
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
        p2 = (int(self.handler.pos[X]+self.debit*math.cos(self.handler.orientation+self.spray)), int(self.handler.pos[Y]+self.debit*math.sin(self.handler.orientation+self.spray)))
        p3 = (int(self.handler.pos[X]+self.debit*math.cos(self.handler.orientation-self.spray)), int(self.handler.pos[Y]+self.debit*math.sin(self.handler.orientation-self.spray)))
        self.waterfront_length = math.sqrt(((p3[X]-p2[X])**2)+((p3[Y]-p2[Y])**2))
        self.waterfront = pygame.Rect(0, 0, self.waterfront_length, 10)
        self.waterfront.center = (int(self.handler.pos[X]+self.debit), int(self.handler.pos[Y]+self.debit))

        unit.spraying = True
        self.watercone = [self.hose_p, p2, p3]
        # if self.water == []:
        self.spray_actual_water()

    def spray_actual_water(self):
        nbr_water_entities = int(self.spray*50)
        direction = self.handler.orientation - self.spray -(self.spray*2/nbr_water_entities)
        for water in range(0, nbr_water_entities+1, 1):
            direction += self.spray*2/nbr_water_entities
            class_water.Water(self, direction)

    def set_hose_spray(self, input):
        self.spray += (math.pi/100)*input
        if self.spray < self.min_spray:
            self.spray = self.min_spray
        elif self.spray > self.max_spray:
            self.spray = self.max_spray
        if self.debit == self.max_debit:
            self.spray = self.spray

    def set_hose_debit(self, input):
        self.debit += 10*input
        if self.debit < self.min_debit:
            self.debit = self.min_debit
        elif self.debit > self.max_debit:
            self.debit = self.max_debit

    def move_water(self):
        for water in self.water:
            water.mov_water()
