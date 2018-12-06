import pygame

X = 0
Y = 1


class Furniture:
    texture = (200, 200, 150)

    def __init__(self, pos, length, width, MAIN, LEVEL, STRUCTURE, ROOM):
        # INIT
        self.MAIN = MAIN
        self.LEVEL = LEVEL
        self.STRUCTURE = STRUCTURE
        self.ROOM = ROOM
        self.burning = False

        # SETTINGS
        self.influence_rad = self.ROOM.GRID_SIZE
        self.pos = pos
        self.length = length
        self.width = width
        self.rect = pygame.Rect(0, 0, self.length, self.width)
        self.rect.center = self.pos
        self.influence_rect = pygame.Rect(0, 0, self.length, self.width)
        self.influence_rect.center = self.pos
        self.influence_max_length = self.ROOM.GRID_SIZE * 5/2
        self.influence_max_width = self.influence_max_length
        self.influence = 1/100
        self.influence_room = self.influence
        self.heat = self.ROOM.heat

        self.ROOM.Furniture.append(self)

    def ignite(self):
        self.burning = True
        self.heat = 81
        self.influence_rect = pygame.Rect(0, 0, self.length + self.influence_rad, self.width + self.influence_rad)
        self.influence_rect.center = self.pos
        self.influence_rad = 0
        self.texture = (255, 0, 0)

    def isHeatingUp(self):
        for other in self.ROOM.Furniture:
            if other.burning:
                return self.rect.collidelist([other.influence_rect]) != -1

    def isCooledDown(self):
        # for water in self.LEVEL.
        pass

    def burn(self):
        if self.burning:
            self.heat += 1/30
            self.ROOM.heat += self.influence_room
        elif self.isHeatingUp():
            self.heat += 1/100
        if self.heat <= 80:
            self.influence_rad = 0
        elif int(self.heat) == 80:
            self.ignite()
        elif 80 <= self.heat < 400:
            if self.influence_rad < self.influence_max_length:
                self.influence_rad += 1/50
                self.influence_room += self.heat//1000
            else:
                self.influence_rad = self.influence_max_length
        elif self.heat >= 400:
            self.influence_rad = self.influence_max_length

        self.influence_rect = pygame.Rect(0, 0, self.length + self.influence_rad, self.width + self.influence_rad)
        self.influence_rect.center = self.pos
