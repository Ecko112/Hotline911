import pygame
import math
import random

X = 0
Y = 1


class Water:

    def __init__(self, hose, direction, LEVEL):
        # INIT
        self.LEVEL = LEVEL
        self.MAIN = self.LEVEL.MAIN
        self.SCREEN = self.LEVEL.SCREEN
        self.parent_hose = hose
        self.texture = (10, 0, 0)
        # Set water particle
        # rand_modif = random.randrange(-10, 10, 1)
        rand_modif = 0
        self.debit = self.parent_hose.debit + rand_modif
        self.pos = [self.parent_hose.hose_p[X], self.parent_hose.hose_p[Y]]
        self.direction = direction
        # Set Rect object
        self.size = self.debit/10
        if self.size > 50:
            self.size = 50
        elif self.size < 10:
            self.size = 10

        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = self.pos
        # Add to level list
        self.LEVEL.Water.append(self)

    def paint_water(self):
        pygame.draw.rect(self.SCREEN, self.texture, self.rect)
        pass

    def move_water(self):
        for structure in self.parent_hose.handler.LEVEL.Structures:
            for wall in structure.Walls:
                if self.rect.colliderect(wall.Rect):
                    self.LEVEL.Water.remove(self)
                    return 'collision mur'
        for structure in self.parent_hose.handler.LEVEL.Structures:
            for room in structure.Rooms:
                for furniture in room.Furniture:
                    if self.rect.colliderect(furniture.rect):
                        self.LEVEL.Water.remove(self)
                        return 'collision object'
        if self.debit > 1:
            if self.debit%2:
                self.texture = (0, 50, 50)
                self.direction += math.pi/10
            else:
                self.texture = (0, 20, 20)
                self.direction -= math.pi/10
            # MRU depending on initial direction
            rand_modif = (1000+(random.randrange(-200, 200, 1)))/1000
            self.pos[X] += 10*math.cos(self.direction)*rand_modif
            self.pos[Y] += 10*math.sin(self.direction)*rand_modif
            self.rect.center = self.pos
            self.debit -= 1
        else:
            self.LEVEL.Water.remove(self)
