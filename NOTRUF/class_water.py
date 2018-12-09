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
        self.debit = self.parent_hose.debit
        self.max_dist = max_dist
        self.spawnpos = [self.parent_hose.hose_p[X], self.parent_hose.hose_p[Y]]
        self.pos = self.spawnpos
        self.rand_modif = (100 + (random.randrange(-20, 20, 1))) / 100
        # [DEV] Disable Randomized Water Movement
        # self.rand_modif = 1
        self.direction = direction
        # Set Rect object
        self.size = 15

        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = self.spawnpos
        # Add to level list
        self.LEVEL.Water.append(self)
        # print(self.max_dist)
        # print(self.debit)

    def paint_water(self):
        pygame.draw.rect(self.SCREEN, self.texture, self.rect)
        pass

    def move_water(self):
        # for structure in self.parent_hose.handler.LEVEL.Structures:
        #     for wall in structure.Walls:
        #         if self.rect.colliderect(wall.Rect):
        #             self.LEVEL.Water.remove(self)
        #             return 'collision mur'
        # for structure in self.parent_hose.handler.LEVEL.Structures:
        #     for room in structure.Rooms:
        #         for furniture in room.Furniture:
        #             if self.rect.colliderect(furniture.rect):
        #                 self.LEVEL.Water.remove(self)
        #                 return 'collision object'
        for structure in self.LEVEL.Structures:
            if collision(self, structure.Walls):
                self.LEVEL.Water.remove(self)
                return
        if get_dist(self.parent_hose.hose_p, self.pos) < self.max_dist:
            if self.debit%2:
                self.texture = (80, 159, 239)
            else:
                self.texture = (70, 140, 210)
            # MRU depending on initial direction
            self.pos[X] += 20*math.cos(self.direction*(math.pi/180))*self.rand_modif
            self.pos[Y] += 20*math.sin(self.direction*(math.pi/180))*self.rand_modif
            self.rect.center = self.pos
            self.debit -= 1
        else:
            self.LEVEL.Water.remove(self)


def collision(objet, liste):
    return objet.rect.collidelist([o.Rect for o in liste]) != -1


def get_dist(point1, point2):
    return int(math.sqrt(((point1[X]-point2[X])**2)+(point1[Y]-point2[Y])**2))
