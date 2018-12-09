import pygame

pygame.font.init()

X = 0
Y = 1


class Furniture:
    texture = (200, 200, 150)
    font = pygame.font.SysFont('monospace', 20)

    ignition_tresh = 80

    def __init__(self, pos, length, width, ROOM):
        # INIT
        self.ROOM = ROOM
        self.SCREEN = self.ROOM.SCREEN
        self.STRUCTURE = self.ROOM.STRUCTURE
        self.LEVEL = self.ROOM.LEVEL
        self.MAIN = self.ROOM.LEVEL
        self.burning = False

        # SETTINGS
        self.pos = pos
        self.length = length
        self.width = width
        self.Rect = pygame.Rect(0, 0, self.length, self.width)
        self.Rect.center = self.pos

        self.influence_rect = pygame.Rect(0, 0, self.length, self.width)
        self.influence_rect.center = self.pos

        self.influence_rad = self.ROOM.GRID_SIZE
        self.influence_max = self.ROOM.GRID_SIZE * 5 / 2
        self.influence = 1/100
        self.influence_room = self.influence
        self.temp = self.ROOM.temp

        self.ROOM.Furniture.append(self)
        self.STRUCTURE.Furniture.append(self)

    def paint_furniture(self):
        pygame.draw.rect(self.SCREEN, self.texture, self.Rect)
        # [DEV] DRAW RADIATION ZONE
        pygame.draw.rect(self.SCREEN, (0, 0, 0), self.influence_rect, 2)

    def ignite(self):
        self.burning = True
        self.temp = self.ignition_tresh
        self.influence_rect = pygame.Rect(0, 0, self.length + self.influence_rad, self.width + self.influence_rad)
        self.influence_rect.center = self.pos
        self.influence_rad = 0
        self.texture = (255, 0, 0)

    def isHeatingUp(self):
        for other in self.ROOM.Furniture:
            if other.burning:
                return self.Rect.collidelist([other.influence_rect]) != -1

    def isCooledDown(self):
        # for water in self.LEVEL.
        pass

    def burn(self):
        if self.burning:
            self.temp += 1 / 30
            self.ROOM.temp += self.influence_room
        elif self.isHeatingUp():
            self.temp += 1 / 100
        if self.temp <= self.ignition_tresh:
            self.influence_rad = 0
        elif int(self.temp) == self.ignition_tresh:
            self.ignite()
        elif self.ignition_tresh <= self.temp < 400:
            if self.influence_rad < self.influence_max:
                self.influence_rad += 1/50
                self.influence_room += self.temp // 100
            else:
                self.influence_rad = self.influence_max
        elif 400 <= self.temp:
            self.influence_rad = self.influence_max

        self.influence_rect = pygame.Rect(0, 0, self.length + self.influence_rad, self.width + self.influence_rad)
        self.influence_rect.center = self.pos
