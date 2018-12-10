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
        self.area = self.length*self.width
        self.grid_area = int(self.area/(self.ROOM.GRID_SIZE**2))
        self.Rect = self.influence_Rect = pygame.Rect(0, 0, self.length, self.width)
        self.Rect.center = self.influence_Rect.center = self.pos

        self.influence_rad = self.STRUCTURE.GRID_SIZE
        self.influence_rad_max = self.STRUCTURE.GRID_SIZE * 3
        self.influence = 1/100
        self.influence_room = self.influence
        self.temp = self.ROOM.temp

        self.ROOM.Furniture.append(self)
        self.STRUCTURE.Furniture.append(self)

    def paint_furniture(self):
        pygame.draw.rect(self.SCREEN, self.texture, self.Rect)
        # [DEV] DRAW RADIATION ZONE
        pygame.draw.rect(self.SCREEN, (0, 0, 0), self.influence_Rect, 2)

    def ignite(self):
        self.burning = True
        self.temp = self.ignition_tresh
        self.texture = (255, 0, 0)
        pass

    def isHeatingUp(self):
        for other in self.STRUCTURE.Furniture:
            if other.burning:
                return self.Rect.collidelist([other.influence_Rect]) != -1

    def cool_down(self, effect):
        self.temp -= effect/self.grid_area*2
        # if self.temp < 30:
        #     self.temp = 30

    def burn(self):
        if self.temp < 30:
            self.temp = 30
        elif self.temp > 700:
            self.temp = 600
        if self.burning:
            if self.temp < 700:
                self.temp += 1/self.grid_area
        else:
            if self.isHeatingUp():
                self.temp += 0.1
            else:
                if self.temp > self.ROOM.temp:
                    self.temp -= 0.1
            if self.temp-2 <= self.ignition_tresh <= self.temp+2:
                self.ignite()
        self.update_influence()
        self.update_rect()
        # print(self.temp)

    def update_rect(self):
        self.influence_Rect = pygame.Rect(0, 0, self.length + self.influence_rad, self.width + self.influence_rad)
        self.influence_Rect.center = self.pos
        if self.temp <= self.ignition_tresh:
            self.texture = (0, 0, 255)
        elif 30 < self.temp <= 255:
            self.texture = (self.temp, 0, 0)
        else:
            self.texture = (255, 0, 0)

    def update_influence(self):
        if self.burning:
            self.influence = self.temp//10
            self.influence_rad = self.influence * 2

            # if self.influence*2 <= self.influence_rad_max:
