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
        self.Rect = self.influence_Rect = pygame.Rect(0, 0, self.length, self.width)
        self.Rect.center = self.influence_Rect.center = self.pos

        self.influence_rad = self.STRUCTURE.GRID_SIZE
        self.influence_max = self.ROOM.GRID_SIZE * 5 / 2
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
        self.texture = (255, 0, 0)
        pass

    def isHeatingUp(self):
        for other in self.ROOM.Furniture:
            if other.burning:
                return self.Rect.collidelist([other.influence_rect]) != -1

    def isCooledDown(self):
        pass

    def burn(self):
        pass
