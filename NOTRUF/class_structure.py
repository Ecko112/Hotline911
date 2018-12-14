import random
import pygame
import class_room

X = 0
Y = 1


class Structure:

    def __init__(self, level):
        # INIT
        self.LEVEL = level
        self.MAIN = self.LEVEL.MAIN
        self.SCREEN = self.LEVEL.SCREEN
        self.wall_texture = (170, 160, 160)
        # Lists
        self.Rooms = []
        self.Separation = []
        self.Walls = []
        self.Doormats = []
        self.Furniture = []
        # Booleans
        self.add_one_floor_1 = True
        self.last_one_floor_1 = False
        self.add_one_floor_2 = True
        self.burning = False
        # Variables
        self.nb_rooms_level_1 = 0
        # LONGUEURS
        self.MIN_ROOM = self.LEVEL.MIN_ROOM
        self.GRID_SIZE = self.LEVEL.GRID_SIZE
        self.DOOR_SIZE = self.LEVEL.DOOR_SIZE
        self.ZONE_LENGTH = random.randrange(10*self.GRID_SIZE, 48*self.GRID_SIZE, self.GRID_SIZE)
        self.ZONE_WIDTH = self.LEVEL.ZONE[Y]
        # [DEV] FORCE LARGE_BUILDING
        # self.ZONE_LENGTH = 48*self.GRID_SIZE
        self.WALL_SIZE = self.MIN_ROOM // 15
        # POINTS
        self.UPPER_LEFT = self.LEVEL.UPPER_LEFT
        self.UPPER_RGHT = (self.UPPER_LEFT[X] + self.ZONE_LENGTH, 0)
        self.LOWER_LEFT = (self.UPPER_LEFT[X], self.UPPER_LEFT[Y] + self.ZONE_WIDTH)
        self.LOWER_RGHT = (self.UPPER_LEFT[X] + self.ZONE_LENGTH, self.UPPER_LEFT[Y] + self.ZONE_WIDTH)
        # FONCTIONS
        self.create_level_1()
        self.create_level_2(self.Separation[0])
        self.wall_up()
        self.stuff_up()
        # SAVE
        self.LEVEL.Structures.append(self)

    def ignite(self):
        self.burning = True
        # Ignite ONE random room
        self.Rooms[random.randint(0, len(self.Rooms)-1)].ignite()

    def burn(self):
        if self.burning:
            for room in self.Rooms:
                room.burn()

    def add_room(self, room):
        self.Rooms.append(room)
        room.get_a_rect()

    def wall_up(self):
        # This Function creates Wall instance
        # Create Upper Wall
        wall_h = class_room.Wall()
        wall_h.p1 = (self.UPPER_LEFT[X] - self.WALL_SIZE // 2, self.UPPER_LEFT[Y] - self.WALL_SIZE // 2)
        wall_h.length = self.ZONE_LENGTH + self.WALL_SIZE
        wall_h.width = self.WALL_SIZE
        wall_h.Rect = pygame.Rect(wall_h.p1[X], wall_h.p1[Y], wall_h.length, wall_h.width)
        self.Walls.append(wall_h)
        # Create Left Wall
        wall_v = class_room.Wall()
        wall_v.p1 = (self.UPPER_LEFT[X] - self.WALL_SIZE // 2, self.UPPER_LEFT[Y] - self.WALL_SIZE // 2)
        wall_v.length = self.WALL_SIZE
        wall_v.width = self.ZONE_WIDTH + self.WALL_SIZE
        wall_v.Rect = pygame.Rect(wall_v.p1[X], wall_v.p1[Y], wall_v.length, wall_v.width)
        self.Walls.append(wall_v)

        for room in self.Rooms:
            room.wall_up()

    def create_level_1(self):
        # INIT
        report = 0
        i = 1
        # Remember Separation
        mid = Separation()
        self.Separation.append(mid)
        # Create Rooms
        while self.add_one_floor_1:
            # Create ONE room
            room = class_room.Room(self)
            if not self.last_one_floor_1:
                # Cas général :
                # lengthprim = random
                room.lengthprim = random.randrange(self.MIN_ROOM, 20*self.GRID_SIZE, self.GRID_SIZE)
                # widthprim = random
                room.widthprim = random.randrange(self.MIN_ROOM, self.ZONE_WIDTH - self.MIN_ROOM, self.GRID_SIZE)
                # Vérification pour rajouter une pièce
                self.check_room_left(room, report)
            if self.last_one_floor_1:
                # Cas particulier :
                # Il n'y a plus de place pour mettre
                # une pièce entière après celle-ci
                self.add_one_floor_1 = False
                self.nb_rooms_level_1 = i
                # lengthprim = prédeterminée par les autres pièces
                room.lengthprim = self.ZONE_LENGTH - report
                # widthprim = random
                room.widthprim = random.randrange(self.MIN_ROOM, self.ZONE_WIDTH - self.MIN_ROOM, 25)
            # Calculer les points
            room.p1 = (self.UPPER_LEFT[X] + report, self.UPPER_LEFT[Y])
            room.p2 = (room.p1[X] + room.lengthprim, room.p1[Y])
            room.p3 = (room.p2[X], room.p2[Y] + room.widthprim)
            room.p4 = (room.p3[X] - room.lengthprim, room.p3[Y])
            # [DEPRECATED]
            # Calcul Mid_point
            if room.lengthprim >= (self.MIN_ROOM * 2):
                mid_length = random.randrange(room.p4[X] + (self.MIN_ROOM - 50), room.p3[X] - (self.MIN_ROOM - 50), 10)
                mid_point = (mid_length, room.p4[Y])
            else:
                mid_point = None
            mid.add_point(room.p3, room.p4, mid_point)
            # Noter les longueurs et largeurs
            room.lengthsec = 0
            room.length = room.lengthprim
            room.widthsec = 0
            room.width = room.widthprim
            room.shape = 'rect'
            # Enregistrer
            self.add_room(room)
            # Reporter
            report += room.lengthprim
            i += 1

    def create_level_2(self, separation):

        i = self.nb_rooms_level_1 + 1
        j = 0
        # next_p = separation.List[0][0]
        shapes = ('rect', 'poly')

        while self.add_one_floor_2:
            room = class_room.Room(self)
            # Randomize shape (50/50)
            room.shape = random.choice(shapes)
            if j >= self.nb_rooms_level_1 - 1:
                # Last Room is always a Rectangle
                room.shape = 'rect'

            if room.shape == 'rect':
                # CAS RECTANGLE
                # Reprendre les longueurs
                room.lengthprim = (separation.List[j][1][X] - separation.List[j][0][X])
                room.widthprim = (self.LOWER_LEFT[Y] - separation.List[j][0][Y])
                room.length = room.lengthsec = room.lengthprim
                room.width = room.widthsec = room.widthprim
                # Set points
                room.p1 = separation.List[j][0]
                room.p2 = (room.p1[X] + room.lengthprim, room.p1[Y])
                room.p3 = (room.p2[X], room.p2[Y] + room.widthprim)
                room.p4 = (room.p3[X] - room.lengthprim, room.p3[Y])
                # Incrémentation
                j += 1

            elif room.shape == 'poly':
                # CAS POLYGONE
                # Set points
                room.p1 = separation.List[j][0]
                room.p2 = separation.List[j][1]
                room.p3 = separation.List[j+1][0]
                room.p4 = separation.List[j+1][1]
                room.p5 = (room.p4[X], self.LOWER_LEFT[Y])
                room.p6 = (room.p1[X], self.LOWER_LEFT[Y])
                # Noter longueurs et largeurs
                room.lengthprim = room.p3[X] - room.p1[X]
                room.lengthsec = room.p5[X] - room.p3[X]
                room.length = room.p5[X] - room.p1[X]
                room.widthprim = room.p3[Y] - room.p1[Y]
                room.widthsec = room.p5[Y] - room.p3[Y]
                room.width = room.p5[Y] - room.p1[Y]
                # Incrémentation double car un polygone prend
                # deux pièces
                j += 2
            # Enregistrer pièce
            self.add_room(room)
            i += 1
            if i == (self.nb_rooms_level_1 * 2) + 1 or j >= self.nb_rooms_level_1:
                self.add_one_floor_2 = False

    def check_room_left(self, room, report):
        # Cette fonction vérfie qu'il y aura assez
        # de place pour la pièce suivante
        # et Reroll si ce n'est pas le cas

        # INIT
        j = 0
        check = True
        # Premier Calcul
        room_left = self.ZONE_LENGTH - (report + room.lengthprim)
        # Vérifier tant que la longueur restante < la longueur minimale
        while check and room_left < self.MIN_ROOM:
            j += 1
            if room.lengthprim == self.MIN_ROOM:
                check = False
                self.last_one_floor_1 = True
            elif j == 50:
                # Limiter à 50 essais
                # Il est impossible de mettre une pièce après
                # La pièce va donc fermer la ZONE
                room.lengthprim = self.ZONE_LENGTH - report
                # C'est la dernière itération de la boucle
                self.add_one_floor_1 = False
                check = False
            else:
                # Reroll dans un plus petit range()
                room.lengthprim = random.randrange(self.MIN_ROOM, room.lengthprim, self.GRID_SIZE)
                check = True
            # Actualiser valeur
            room_left = self.ZONE_LENGTH - (report + room.lengthprim)

    def paint_structure(self):
        for room in self.Rooms:
            room.paint_room()
        for wall in self.Walls:
            pygame.draw.rect(self.SCREEN, self.wall_texture, wall.Rect)

    def stuff_up(self):
        for room in self.Rooms:
            room.stuff_up()


class Separation:
    # List of lower points of rooms from Floor_1
    # Ignorer mid_point
    def __init__(self):
        self.List = []

    def add_point(self, point3, point4, mid_point):
        self.List.append((point4, point3, mid_point))
