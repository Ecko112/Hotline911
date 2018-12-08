import pygame
import math
import random

X = 0
Y = 1


class Water:

    def __init__(self, hose, direction, max_dist, LEVEL):
        # INIT
        self.LEVEL = LEVEL
        self.MAIN = self.LEVEL.MAIN
        self.SCREEN = self.LEVEL.SCREEN
        self.parent_hose = hose
        self.texture = (10, 0, 0)
        # Set water particle
        # rand_modifdebit = (1000 + (random.randrange(-200, 200, 1)))/1000
        self.debit = self.parent_hose.debit
        self.max_dist = max_dist
        self.spawnpos = [self.parent_hose.hose_p[X], self.parent_hose.hose_p[Y]]
        self.pos = self.spawnpos
        self.direction = direction
        # Set Rect object
        self.size = 10
        # if self.size > 50:
        #     self.size = 50
        # elif self.size < 10:
        #     self.size = 10

        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = self.spawnpos
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
        if get_dist(self.spawnpos, self.pos) < self.max_dist:
            print(self.pos)
            print(self.spawnpos)
            print(get_dist(self.spawnpos, self.pos), self.max_dist)
            if self.debit%2:
                self.texture = (0, 50, 50)
            else:
                self.texture = (0, 20, 20)
            # MRU depending on initial direction
            rand_modif = (1000+(random.randrange(-200, 200, 1)))/1000
            # rand_modif = 1
            self.pos[X] += 10*math.cos(self.direction*(math.pi/180))*rand_modif
            self.pos[Y] += 10*math.sin(self.direction*(math.pi/180))*rand_modif
            self.rect.center = self.pos
        else:
            self.LEVEL.Water.remove(self)


def get_dist(point1, point2):
    return int(math.sqrt(((point1[X]-point2[X])**2)+(point1[Y]-point2[Y])**2))
