import pygame
import math

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
        print('entré pour ', nbr_water_entities, 'itération(s)')
        for water in range(0, nbr_water_entities+1, 1):
            print("iteration = ", water)
            direction += self.spray*2/nbr_water_entities
            print(direction)
            Water(self, direction)

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


class Water:
    debit = 20
    spawnpoint = [0, 0]

    def __init__(self, hose, direction):
        self.parent_hose = hose
        self.direction = direction
        self.debit = self.parent_hose.debit
        self.parent_hose.water.append(self)
        self.spawnpoint = [self.parent_hose.hose_p[X], self.parent_hose.hose_p[Y]]

        self.rect = pygame.Rect(0, 0, self.debit/5, self.debit/5)
        self.pos = self.spawnpoint
        self.rect.center = self.pos
        print(self.rect.center)

    def draw_water(self, screen):
        pygame.draw.rect(screen, texture, self.rect)

    def move_water(self):
        screen = self.parent_hose.handler.MAIN.screen
        for structure in self.parent_hose.handler.LEVEL.Structures:
            for wall in structure.Walls:
                if self.rect.colliderect(wall.Rect):
                    self.parent_hose.water.remove(self)
                    return 'collision'

        if self.debit > 1:
            if self.debit%2:
                texture = (0, 50, 50)
            else:
                texture = (0, 20, 20)
            self.pos[X] += 10*math.cos(self.direction)
            self.pos[Y] += 10*math.sin(self.direction)
            self.rect.center = self.pos
            pygame.draw.rect(screen, texture, self.rect)
            self.debit -= 1
        elif -5 <= self.debit <= 1:
            texture = (255, 0, 255)
            self.pos[X] -= 10*math.cos(self.direction)
            self.pos[Y] -= 10*math.sin(self.direction)
            self.rect.center = self.pos
            pygame.draw.rect(screen, texture, self.rect)
            self.debit -= 1
        elif -30 <= self.debit < -5:
            self.debit -= 1
        else:
            self.parent_hose.water.remove(self)




