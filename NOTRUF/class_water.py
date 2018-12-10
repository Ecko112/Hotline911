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
        # Set Rect object
        if self.parent_hose.spray == self.parent_hose.spray_presets[0]:
            self.size = random.randrange(15, 25, 1)
            self.solid_effect = self.size / 5
            self.room_effect = (30 - self.size) / 100
        elif self.parent_hose.spray == self.parent_hose.spray_presets[1]:
            self.size = random.randrange(10, 15, 1)
            self.solid_effect = self.size / 50
            self.room_effect = (25 - self.size) / 75
        elif self.parent_hose.spray == self.parent_hose.spray_presets[2]:
            self.size = random.randrange(3, 10, 1)
            self.solid_effect = self.size / 75
            self.room_effect = (25 - self.size) / 50
        self.Rect = pygame.Rect(0, 0, self.size, self.size)
        # Set water particle
        self.life = self.parent_hose.debit
        self.max_dist = max_dist
        self.spawnpos = [self.parent_hose.hose_p[X], self.parent_hose.hose_p[Y]]
        self.pos = self.spawnpos
        self.Rect.center = self.spawnpos
        # Set water particle effects on temp

        # Randomize Water Movement
        self.rand_modif = (100 + (random.randrange(-20, 20, 1))) / 100
        # [DEV] Disable Randomized Water Movement
        # self.rand_modif = 1
        self.direction = direction
        # Add to level list
        self.LEVEL.Water.append(self)

    def paint_water(self):
        pygame.draw.rect(self.SCREEN, self.texture, self.Rect)

    def move_water(self):
        for structure in self.LEVEL.Structures:
            for wall in structure.Walls:
                if self.Rect.colliderect(wall.Rect):
                    self.LEVEL.Water.remove(self)
                    return
            for room in structure.Rooms:
                for objet in room.Furniture:
                    if self.Rect.colliderect(objet.Rect):
                        room.cool_down(self.room_effect)
                        objet.cool_down(self.solid_effect)
                        self.LEVEL.Water.remove(self)
                        return
        if get_dist(self.parent_hose.hose_p, self.pos) < self.max_dist:
            if self.life%2:
                self.texture = (80, 159, 239)
            else:
                self.texture = (70, 140, 210)
            # MRU depending on initial direction
            self.pos[X] += 20*math.cos(self.direction*(math.pi/180))*self.rand_modif
            self.pos[Y] += 20*math.sin(self.direction*(math.pi/180))*self.rand_modif
            self.Rect.center = self.pos
            self.life -= 1
        else:
            self.LEVEL.Water.remove(self)


def collision(objet, liste):
    return objet.rect.collidelist([o.Rect for o in liste]) != -1


def get_dist(point1, point2):
    return int(math.sqrt(((point1[X]-point2[X])**2)+(point1[Y]-point2[Y])**2))
