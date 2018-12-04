import pygame
import math

X = 0
Y = 1


class Water:
    debit = 20
    spawnpos = [0, 0]

    def __init__(self, hose, direction):
        self.parent_hose = hose
        self.direction = direction
        self.debit = self.parent_hose.debit
        self.parent_hose.water.append(self)
        self.spawnpos = [self.parent_hose.hose_p[X], self.parent_hose.hose_p[Y]]

        self.rect = pygame.Rect(0, 0, self.debit/5, self.debit/5)
        self.pos = self.spawnpos
        self.rect.center = self.pos

    def draw_water(self, screen):
        pygame.draw.rect(screen, texture, self.rect)

    def move_water(self):
        screen = self.parent_hose.handler.MAIN.screen
        for structure in self.parent_hose.handler.LEVEL.Structures:
            for wall in structure.Walls:
                if self.rect.colliderect(wall.Rect):
                    self.parent_hose.water.remove(self)
                    return 'collision mur'
        for structure in self.parent_hose.handler.LEVEL.Structures:
            for room in structure.Rooms:
                for furniture in room.Furniture:
                    if self.rect.colliderect(furniture.rect):
                        self.parent_hose.water.remove(self)
                        return 'collision object'
        if self.debit > 1:
            if self.debit%2:
                texture = (0, 50, 50)
                # self.direction += math.pi/2
            else:
                texture = (0, 20, 20)
                # self.direction -= math.pi/2
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
        else:
            self.parent_hose.water.remove(self)
