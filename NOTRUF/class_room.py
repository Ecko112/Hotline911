import pygame
import random
import class_furniture


X = 0
Y = 1

t = 0


class Room:
    # Textures
    floor_texture = (168, 119, 90)
    wall_texture = (170, 160, 0)

    def __init__(self, STRUCTURE):
        # INIT
        self.STRUCTURE = STRUCTURE
        self.LEVEL = self.STRUCTURE.LEVEL
        self.MAIN = self.LEVEL.MAIN
        self.SCREEN = self.STRUCTURE.SCREEN
        self.WALL_SIZE = self.STRUCTURE.WALL_SIZE
        self.GRID_SIZE = self.STRUCTURE.GRID_SIZE
        # Lists
        self.Walls = []
        self.Furniture = []
        self.Burning = []
        # Dimensions
        self.lengthprim = None
        self.lengthsec = None
        self.length = None
        self.widthprim = None
        self.width = None
        self.widthsec = None
        # Points
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
        self.p5 = None
        self.p6 = None
        self.polyroom = []
        self.shape = None
        # SET DEFAULT
        self.on_fire = False
        self.temp = 30
        # OTHER
        self.temp_font_size = 40
        self.temp_font = pygame.font.SysFont('monospace', self.temp_font_size)
        self.temp_message = self.temp_font.render(str(self.temp), False, (0, 0, 0))

    def ignite(self):
        self.on_fire = True
        # IGNITE A RANDOM OBJECT IN THE ROOM
        self.Furniture[random.randint(0, len(self.Furniture)-1)].ignite()

    def burn(self):
        if len(self.Burning) == 0:
            self.on_fire = False
        for object in self.Furniture:
            object.burn()
            if object.burning:
                self.on_fire = True
                # Increase Room temp
                # Based on room.size and object size
                self.temp += 0.1/self.grid_area*object.grid_area
        if self.on_fire:
            if 400 <= int(self.temp) <= 401:
                self.flashover()
        else:
            if 30 < self.temp:
                self.temp -= 1/self.grid_area

    def cool_down(self, effect):
        # Decrease Room Temp
        # based on room.area and hose.spray
        temp = self.temp - effect/self.grid_area
        if temp > 60:
            self.temp = temp

    def flashover(self):
        # Auto-ignition of all the objects in the room
        for object in self.Furniture:
            object.ignite()
            object.temp = 400
        self.floor_texture = (230, 0, 0)

    def poly_room(self):
        # Gather points in a list
        self.polyroom = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]

    def paint_room(self):
        self.poly_room()
        pygame.draw.polygon(self.SCREEN, self.floor_texture, self.polyroom)
        for objet in self.Furniture:
            objet.paint_furniture()
        # [DEV] BLIT TEMPERATURE
        # global t
        # if t == 10:
        #     self.temp_message = self.temp_font.render(str(self.temp), False, (0, 0, 0))
        #     t = 0
        # else:
        #     t += 1
        # self.SCREEN.blit(self.temp_message, self.p1)

    def stuff_up(self):
        nbr_meubles = random.randint(1, 5)
        while len(self.Furniture) < nbr_meubles:
            # Randomize Size
            object_length = random.randrange(self.GRID_SIZE, abs(self.length) // 2, self.GRID_SIZE)
            object_width = random.randrange(self.GRID_SIZE, abs(self.width) // 2, self.GRID_SIZE)
            # Randomize Position
            posx = random.randrange(object_length // 2, abs(self.length) + 1 - object_length // 2, self.GRID_SIZE)
            posy = random.randrange(object_width // 2, abs(self.width) + 1 - object_width // 2, self.GRID_SIZE)
            position = [posx + self.p1[X], self.p1[Y] + posy]
            # Create Instance
            class_furniture.Furniture(position, object_length, object_width, self)

    def get_a_rect(self):
        # Create a Rect of the room
        self.area = ((self.lengthprim*self.widthprim)+(self.lengthsec*self.widthsec))
        self.grid_area = int(self.area/(self.GRID_SIZE**2))
        self.Rect = pygame.Rect(self.p1[X], self.p1[Y], self.length, self.width)

    def wall_up(self):
        self.poly_room()
        if self.shape == 'rect':
            # MURS HORIZONTAUX
            if self.length > self.STRUCTURE.DOOR_SIZE + 4*self.WALL_SIZE:
                # I can fit a door
                # I need two wall instances
                wall_h11 = Wall()
                wall_h11.p1 = (self.p4[X] - self.WALL_SIZE // 2, self.p4[Y] - self.WALL_SIZE // 2)
                wall_h11.length = random.randrange(2*self.WALL_SIZE, self.length - self.STRUCTURE.DOOR_SIZE - self.WALL_SIZE*2, self.WALL_SIZE)
                wall_h11.width = self.WALL_SIZE
                self.add_wall(wall_h11)
                # I must put a zone so furniture doesn't block the door
                doormat = Doormat()
                doormat.p1 = [wall_h11.Rect.right, wall_h11.Rect.topright[Y]-self.GRID_SIZE]
                doormat.length = self.STRUCTURE.DOOR_SIZE
                doormat.width = self.GRID_SIZE*2+self.WALL_SIZE
                self.add_doormat(doormat)
                # Finish wall
                wall_h12 = Wall()
                wall_h12.p1 = (wall_h11.p1[X] + wall_h11.length + self.STRUCTURE.DOOR_SIZE, wall_h11.p1[Y])
                wall_h12.length = self.length - wall_h11.length - self.STRUCTURE.DOOR_SIZE
                wall_h12.width = self.WALL_SIZE
                self.add_wall(wall_h12)

            else:
                # I can't fit a door
                # Only one wall instance is needed
                wall_h11 = Wall()
                wall_h11.p1 = (self.p4[X] - self.WALL_SIZE // 2, self.p4[Y] - self.WALL_SIZE // 2)
                wall_h11.length = self.WALL_SIZE + self.length
                wall_h11.width = self.WALL_SIZE
                self.add_wall(wall_h11)

            # MUR VERTICAL
            if True:
                # No vertical doors in this version
                wall_v11 = Wall()
                wall_v11.p1 = (self.p2[X] - self.WALL_SIZE // 2, self.p2[Y] - self.WALL_SIZE // 2)
                wall_v11.length = self.WALL_SIZE
                wall_v11.width = self.width + self.WALL_SIZE
                self.add_wall(wall_v11)

        elif self.shape == 'poly':
            # MURS HORIZONTAUX
            if self.length >= self.STRUCTURE.DOOR_SIZE + 4*self.WALL_SIZE:
                # I can fit a door
                # I need two wall instances
                wall_h11 = Wall()
                wall_h11.p1 = (self.p6[X] - self.WALL_SIZE // 2, self.p6[Y] - self.WALL_SIZE // 2)
                wall_h11.length = random.randrange(2*self.WALL_SIZE, self.length - self.STRUCTURE.DOOR_SIZE - 2*self.WALL_SIZE, self.WALL_SIZE)
                wall_h11.width = self.WALL_SIZE
                self.add_wall(wall_h11)
                # I must put a zone so furniture doesn't block the door
                doormat = Doormat()
                doormat.p1 = [wall_h11.Rect.right, wall_h11.Rect.topright[Y] - self.GRID_SIZE]
                doormat.length = self.STRUCTURE.DOOR_SIZE
                doormat.width = self.GRID_SIZE * 2 + self.WALL_SIZE
                self.add_doormat(doormat)
                # Finish Wall
                wall_h12 = Wall()
                wall_h12.p1 = (wall_h11.p1[X] + wall_h11.length + self.STRUCTURE.DOOR_SIZE, wall_h11.p1[Y])
                wall_h12.length = self.length - self.STRUCTURE.DOOR_SIZE - wall_h11.length
                wall_h12.width = self.WALL_SIZE
                self.add_wall(wall_h12)

            else:
                # I can't fit a door
                wall_h11 = Wall()
                wall_h11.p1 = (self.p6[X] - self.WALL_SIZE // 2, self.p6[Y] - self.WALL_SIZE // 2)
                wall_h11.length = self.length + self.WALL_SIZE
                wall_h11.width = self.WALL_SIZE
                self.add_wall(wall_h11)
            # MURS VERTICAUX
            if True:
                # I need two walls because it's a Polygon
                # and therefore has 2 different widths
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

    def add_doormat(self, doormat):
        doormat.get_rect()
        self.STRUCTURE.Doormats.append(doormat)

    def add_wall(self, wall):
        wall.get_rect()
        self.Walls.append(wall)
        self.STRUCTURE.Walls.append(wall)


class Wall:
    # Self-explanatory
    p1 = None
    length = None
    width = None
    Rect = None

    def get_rect(self):
        self.Rect = pygame.Rect(self.p1[X], self.p1[Y], self.length, self.width)


class Doormat:
    # Hitbox to prevent objects to block doors
    p1 = None
    length = None
    width = None
    Rect = None

    def get_rect(self):
        self.Rect = pygame.Rect(self.p1[X], self.p1[Y], self.length, self.width)
