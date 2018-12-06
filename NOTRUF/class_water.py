import pygame
import math

X = 0
Y = 1


class Water:
    debit = 20
    spawnpos = [0, 0]

    def __init__(self, hose, direction, LEVEL):
        # INIT
        self.LEVEL = LEVEL
        self.MAIN = self.LEVEL.MAIN
        self.SCREEN = self.LEVEL.SCREEN
        self.parent_hose = hose
        self.texture = (10, 0, 0)
        # Set water particle
        self.debit = self.parent_hose.debit
        self.pos = [self.parent_hose.hose_p[X], self.parent_hose.hose_p[Y]]
        self.direction = direction
        # Set Rect object
        self.rect = pygame.Rect(0, 0, self.debit/5, self.debit/5)
        self.rect.center = self.pos
        # Add to level list
        self.LEVEL.Water.append(self)

    def paint_water(self):
        pygame.draw.rect(self.SCREEN, self.texture, self.rect)

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
                # self.direction += math.pi/2
            else:
                self.texture = (0, 20, 20)
                # self.direction -= math.pi/2
            # MRU depending on initial direction
            self.pos[X] += 10*math.cos(self.direction)
            self.pos[Y] += 10*math.sin(self.direction)
            self.rect.center = self.pos
            self.debit -= 1
        else:
            self.LEVEL.Water.remove(self)
