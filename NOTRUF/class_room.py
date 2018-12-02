import pygame
import random
from UNDER_PROGRESS import class_furniture
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

    def __init__(self, name, MAIN, LEVEL, STRUCTURE):
        # INIT
        self.name = name
        self.MAIN = MAIN
        self.LEVEL = LEVEL
        self.STRUCTURE = STRUCTURE
        self.burning = False
        self.WALL_SIZE = self.STRUCTURE.WALL_SIZE
        self.GRID_SIZE = self.STRUCTURE.GRID_SIZE
        self.heat = 30

    def ignite(self):
        self.burning = True
        self.Furniture[random.randint(0, len(self.Furniture)-1)].ignite()

    def burn(self):
        if self.burning:
            for object in self.Furniture:
                object.burn()
            if 400 < int(self.heat) < 401:
                self.flashover()

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
        for object in self.Furniture:
            pygame.draw.rect(screen, object.texture, object.rect)
            pygame.draw.rect(screen, (0,0,0), object.influence_rect, 2)

    def stuff_up(self):
        nbr_meubles = random.randint(1, 5)
        for meuble in range(nbr_meubles):
            length = random.randrange(self.GRID_SIZE, abs(self.length) // 2, self.GRID_SIZE)
            width = random.randrange(self.GRID_SIZE, abs(self.width) // 2, self.GRID_SIZE)
            posx = random.randrange(length // 2, abs(self.length) + 1 - length // 2, self.GRID_SIZE)
            posy = random.randrange(width // 2, abs(self.width) + 1 - width // 2, self.GRID_SIZE)
            position = [posx + self.p1[X], self.p1[Y] + posy]

            class_furniture.Furniture(position, length, width, self.MAIN, self.LEVEL, self.STRUCTURE, self)

    def wall_up(self, structure):
        self.poly_room()
        if self.shape == 'rect':
            if self.length > structure.DOOR_SIZE + 50:
                wall_h11 = Wall('wall_h11')
                wall_h11.p1 = (self.p4[X] - self.WALL_SIZE // 2, self.p4[Y] - self.WALL_SIZE // 2)
                wall_h11.length = random.randrange(35, self.length - structure.DOOR_SIZE - 25, 25)
                wall_h11.width = self.WALL_SIZE
                self.add_wall(wall_h11, structure)

                wall_h12 = Wall('wall_h12')
                wall_h12.p1 = (wall_h11.p1[X] + wall_h11.length + structure.DOOR_SIZE, wall_h11.p1[Y])
                wall_h12.length = self.length - wall_h11.length - structure.DOOR_SIZE
                wall_h12.width = self.WALL_SIZE
                self.add_wall(wall_h12, structure)

            else:
                wall_h11 = Wall('wall_h11')
                wall_h11.p1 = (self.p4[X] - self.WALL_SIZE // 2, self.p4[Y] - self.WALL_SIZE // 2)
                wall_h11.length = self.WALL_SIZE + self.length
                wall_h11.width = self.WALL_SIZE
                self.add_wall(wall_h11, structure)

            if self.width > structure.DOOR_SIZE:
                pass
                # wall_v11 = Wall('wall_v11')
                # wall_v11.p1 = (self.p2[X] - self.wall_size//2, self.p2[Y] - self.wall_size//2)
                # wall_v11.length = self.wall_size
                # wall_v11.width = random.randrange(0, self.width - structure.DOOR_SIZE - 30, 10)
                # self.add_wall(wall_v11, structure)
                #
                # wall_v12 = Wall('wall_v12')
                # wall_v12.p1 = (wall_v11.p1[X], wall_v11.p1[Y] + wall_v11.width + structure.DOOR_SIZE)
                # wall_v12.length = self.wall_size
                # wall_v12.width = self.width - wall_v11.width - structure.DOOR_SIZE + self.wall_size
                # self.add_wall(wall_v12, structure)

                # porte = Door()
                # porte.p1 = (wall_v11.p1s[X], wall_v11.p1[Y] + wall_v11.width)
                # porte.length = self.wall_size
                # porte.width = structure.DOOR_SIZE
                # self.add_wall(porte, structure)
                #
                # porte_hitbox = Door()
                # porte_hitbox.p1 = (porte.p1[X] - 5, porte.p1[Y] + structure.DOOR_SIZE//2 + wall_v11.width)
                # porte_hitbox.length = 20
                # porte_hitbox.width = 1
                # porte.passable = False
                # self.add_wall(porte_hitbox, structure)
            if True:
                wall_v11 = Wall('wall_v11')
                wall_v11.p1 = (self.p2[X] - self.WALL_SIZE // 2, self.p2[Y] - self.WALL_SIZE // 2)
                wall_v11.length = self.WALL_SIZE
                wall_v11.width = self.width + self.WALL_SIZE
                self.add_wall(wall_v11, structure)

        elif self.shape == 'poly':
            if self.length >= structure.DOOR_SIZE + 60:
                wall_h11 = Wall('wall_h11')
                wall_h11.p1 = (self.p6[X] - self.WALL_SIZE // 2, self.p6[Y] - self.WALL_SIZE // 2)
                wall_h11.length = random.randrange(30, self.length - structure.DOOR_SIZE - 30, 10)
                wall_h11.width = self.WALL_SIZE
                self.add_wall(wall_h11, structure)

                wall_h12 = Wall('wall_h12')
                wall_h12.p1 = (wall_h11.p1[X] + wall_h11.length + structure.DOOR_SIZE, wall_h11.p1[Y])
                wall_h12.length = self.length - structure.DOOR_SIZE - wall_h11.length
                wall_h12.width = self.WALL_SIZE
                self.add_wall(wall_h12, structure)

            else:
                wall_h11 = Wall('wall_h11')
                wall_h11.p1 = (self.p6[X] - self.WALL_SIZE // 2, self.p6[Y] - self.WALL_SIZE // 2)
                wall_h11.length = self.length + self.WALL_SIZE
                wall_h11.width = self.WALL_SIZE
                self.add_wall(wall_h11, structure)

            wall_v11 = Wall('wall_v11')
            wall_v11.p1 = (self.p2[X] - self.WALL_SIZE // 2, self.p2[Y] - self.WALL_SIZE // 2)
            wall_v11.length = self.WALL_SIZE
            wall_v11.width = self.widthprim + self.WALL_SIZE
            self.add_wall(wall_v11, structure)

            wall_v12 = Wall('wall_v12')
            wall_v12.p1 = (self.p4[X] - self.WALL_SIZE // 2, self.p4[Y] - self.WALL_SIZE // 2)
            wall_v12.length = self.WALL_SIZE
            wall_v12.width = self.widthsec + self.WALL_SIZE
            self.add_wall(wall_v12, structure)

    def add_wall(self, wall, structure):
        wall.Rect = pygame.Rect(wall.p1[X], wall.p1[Y], wall.length, wall.width)
        self.Walls.append(wall)
        structure.Walls.append(wall)


class Wall:
    p1 = None
    length = None
    width = None
    Rect = None

    def __init__(self, name):
        self.name = name


# class Door:
#     p1 = None
#     length = None
#     width = None
#     Rect = None
#     passable = False
