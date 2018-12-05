import pygame
import random
from NOTRUF import class_furniture

X = 0
Y = 1


class Room:
    # Lists
    Walls = []
    Furniture = []
    # Dimensions
    length = None
    width = None
    lengthsec = None
    widthsec = None
    lengthprim = None
    widthprim = None
    # Points
    p1 = None
    p2 = None
    p3 = None
    p4 = None
    p5 = None
    p6 = None
    polyroom = []
    shape = None
    # Textures
    floor_texture = (0, 255, 0)
    wall_texture = (255, 255, 255)
    # Furniture

    def __init__(self, STRUCTURE):
        # INIT
        self.STRUCTURE = STRUCTURE
        self.LEVEL = self.STRUCTURE.LEVEL
        self.MAIN = self.LEVEL.MAIN
        self.WALL_SIZE = self.STRUCTURE.WALL_SIZE
        self.GRID_SIZE = self.STRUCTURE.GRID_SIZE
        # SET DEFAULT
        self.burning = False
        self.temp = 30

    def ignite(self):
        self.burning = True
        # IGNITE A RANDOM OBJECT IN THE ROOM
        self.Furniture[random.randint(0, len(self.Furniture)-1)].ignite()

    def burn(self):
        if self.burning:
            for object in self.Furniture:
                object.burn()
            if 400 < int(self.temp) < 401:
                self.flashover()
        else:
            pass

    def flashover(self):
        for object in self.Furniture:
            object.ignite()
            object.heat = 400 + 1

    def poly_room(self):
        self.polyroom = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]

    def paint_room(self, screen):
        self.poly_room()
        pygame.draw.polygon(screen, self.floor_texture, self.polyroom)

    def paint_furniture(self, screen):
        for objet in self.Furniture:
            pygame.draw.rect(screen, objet.texture, objet.rect)
            # [DEV] DRAW RADIATION ZONE
            pygame.draw.rect(screen, (0, 0, 0), objet.influence_rect, 2)

    def stuff_up(self):
        nbr_meubles = random.randint(1, 5)
        for meuble in range(nbr_meubles):
            length = random.randrange(self.GRID_SIZE, abs(self.length) // 2, self.GRID_SIZE)
            width = random.randrange(self.GRID_SIZE, abs(self.width) // 2, self.GRID_SIZE)
            posx = random.randrange(length // 2, abs(self.length) + 1 - length // 2, self.GRID_SIZE)
            posy = random.randrange(width // 2, abs(self.width) + 1 - width // 2, self.GRID_SIZE)
            position = [posx + self.p1[X], self.p1[Y] + posy]

            class_furniture.Furniture(position, length, width, self.MAIN, self.LEVEL, self.STRUCTURE, self)

    def wall_up(self):
        self.poly_room()
        if self.shape == 'rect':
            if self.length > self.STRUCTURE.DOOR_SIZE + 50:
                wall_h11 = Wall()
                wall_h11.p1 = (self.p4[X] - self.WALL_SIZE // 2, self.p4[Y] - self.WALL_SIZE // 2)
                wall_h11.length = random.randrange(35, self.length - self.STRUCTURE.DOOR_SIZE - 25, 25)
                wall_h11.width = self.WALL_SIZE
                self.add_wall(wall_h11)

                wall_h12 = Wall()
                wall_h12.p1 = (wall_h11.p1[X] + wall_h11.length + self.STRUCTURE.DOOR_SIZE, wall_h11.p1[Y])
                wall_h12.length = self.length - wall_h11.length - self.STRUCTURE.DOOR_SIZE
                wall_h12.width = self.WALL_SIZE
                self.add_wall(wall_h12)

            else:
                wall_h11 = Wall()
                wall_h11.p1 = (self.p4[X] - self.WALL_SIZE // 2, self.p4[Y] - self.WALL_SIZE // 2)
                wall_h11.length = self.WALL_SIZE + self.length
                wall_h11.width = self.WALL_SIZE
                self.add_wall(wall_h11)

            if True:
                wall_v11 = Wall()
                wall_v11.p1 = (self.p2[X] - self.WALL_SIZE // 2, self.p2[Y] - self.WALL_SIZE // 2)
                wall_v11.length = self.WALL_SIZE
                wall_v11.width = self.width + self.WALL_SIZE
                self.add_wall(wall_v11)

        elif self.shape == 'poly':
            if self.length >= self.STRUCTURE.DOOR_SIZE + 60:
                wall_h11 = Wall()
                wall_h11.p1 = (self.p6[X] - self.WALL_SIZE // 2, self.p6[Y] - self.WALL_SIZE // 2)
                wall_h11.length = random.randrange(30, self.length - self.STRUCTURE.DOOR_SIZE - 30, 10)
                wall_h11.width = self.WALL_SIZE
                self.add_wall(wall_h11)

                wall_h12 = Wall()
                wall_h12.p1 = (wall_h11.p1[X] + wall_h11.length + self.STRUCTURE.DOOR_SIZE, wall_h11.p1[Y])
                wall_h12.length = self.length - self.STRUCTURE.DOOR_SIZE - wall_h11.length
                wall_h12.width = self.WALL_SIZE
                self.add_wall(wall_h12)

            else:
                wall_h11 = Wall()
                wall_h11.p1 = (self.p6[X] - self.WALL_SIZE // 2, self.p6[Y] - self.WALL_SIZE // 2)
                wall_h11.length = self.length + self.WALL_SIZE
                wall_h11.width = self.WALL_SIZE
                self.add_wall(wall_h11, structure)

            wall_v11 = Wall()
            wall_v11.p1 = (self.p2[X] - self.WALL_SIZE // 2, self.p2[Y] - self.WALL_SIZE // 2)
            wall_v11.length = self.WALL_SIZE
            wall_v11.width = self.widthprim + self.WALL_SIZE
            self.add_wall(wall_v11)

            wall_v12 = Wall()
            wall_v12.p1 = (self.p4[X] - self.WALL_SIZE // 2, self.p4[Y] - self.WALL_SIZE // 2)
            wall_v12.length = self.WALL_SIZE
            wall_v12.width = self.widthsec + self.WALL_SIZE
            self.add_wall(wall_v12)

    def add_wall(self, wall):
        wall.Rect = pygame.Rect(wall.p1[X], wall.p1[Y], wall.length, wall.width)
        self.Walls.append(wall)
        self.STRUCTURE.Walls.append(wall)


class Wall:
    p1 = None
    length = None
    width = None
    Rect = None
