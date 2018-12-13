import class_player
import class_firetruck
import pygame
clock = pygame.time.Clock()

X = 0
Y = 1

tick1 = 0
# This could be a sub to the Level class
# as they share a lot of functionalities
# but ain't nobody got time for that


class Shift:
    ################
    # KEY BINDINGS #
    ################
    # [DEV] FORCE START LEVEL
    FORCE_START_LEVEL = pygame.K_BACKSPACE
    # [DEV] FORCE QUIT LEVEL
    FORCE_QUIT_SHIFT = pygame.K_DELETE
    # Player
    UP = pygame.K_z
    DOWN = pygame.K_s
    LEFT = pygame.K_q
    RGHT = pygame.K_d
    up = left = -1
    down = rght = 1
    GET_IN = pygame.K_e

    def __init__(self, MAIN):
        # INIT
        self.MAIN = MAIN
        self.SCREEN = self.MAIN.SCREEN
        self.SCREEN_RESOLUTION = self.MAIN.SCREEN_RESOLUTION
        self.Units = []
        self.Structures = []
        self.Vehicles = []
        self.intro_is_done = False
        ############
        # TEXTURES #
        ############
        self.HERBE_TEXTURE = self.MAIN.GREEN
        self.BETON_TEXTURE = self.MAIN.LIGHT_GREY
        self.BITUME_TEXTURE = self.MAIN.DARK_GREY
        # PLAYER SETTINGS
        self.PLAYER_SIZE = int(self.SCREEN_RESOLUTION[Y] // 28.4)
        self.STARTING_POS = [8*self.SCREEN_RESOLUTION[X]//10, 8*self.SCREEN_RESOLUTION[Y]//10]
        # STRUCTURE SETTINGS
        self.MIN_ROOM = self.PLAYER_SIZE * 6
        self.DOOR_SIZE = self.PLAYER_SIZE * 3 - 10
        self.GRID_SIZE = self.MIN_ROOM // 6
        # Spawn Player
        self.create_firehouse()
        self.create_player()
        self.engine = class_firetruck.Truck(self)
        self.engine.pos = [230, 225]
        self.engine.image = pygame.transform.rotate(self.engine.image, -90)

    def loop_firehouse(self):
        self.process_input()
        for unit in self.Units:
            unit.get_location_vehicle()
        self.paint_shift()
        # Lock 50 FPS
        clock.tick(50)

    def paint_shift(self):
        # BACKGROUND
        self.SCREEN.fill(self.HERBE_TEXTURE)
        # FIREHOUSE
        for structure in self.Structures:
            structure.paint_structure()
        # VEHICLES
        for vehicle in self.Vehicles:
            vehicle.paint_truck()
        # UNITS
        for unit in self.Units:
            unit.paint_player()
        # Update screen
        pygame.display.flip()

    def process_input(self):
        mouse_pos = pygame.mouse.get_pos()
        for unit in self.Units:
            # ROTATE_PLAYER
            unit.rotate_player(mouse_pos)
            # KEYBOARD INPUT
            key_input = pygame.key.get_pressed()
            # [DEV] FORCE QUIT SHIFT
            if key_input[self.FORCE_QUIT_SHIFT]:
                self.MAIN.create_menu()
            # [DEV] FORCE START LEVEL
            if key_input[self.FORCE_START_LEVEL]:
                self.MAIN.create_level()
            # PLAYER ENTER VEHICLE
            global tick1
            if tick1 <= 20:
                tick1 += 1
            if unit.inDoor and key_input[self.GET_IN] and tick1 >= 20:
                unit.leave_scene()
            # MOVE_PLAYER 4 DIRECTIONS
            if key_input[self.UP]:
                unit.mov_player(self.up, Y)
            elif key_input[self.DOWN]:
                unit.mov_player(self.down, Y)
            if key_input[self.RGHT]:
                unit.mov_player(self.rght, X)
            elif key_input[self.LEFT]:
                unit.mov_player(self.left, X)

    def create_firehouse(self):
        FireStation(self)

    def create_player(self):
        class_player.Player(self)


class FireStation:

    def __init__(self, SHIFT):
        self.LEVEL = SHIFT
        self.MAIN = self.LEVEL.MAIN
        # Lists
        self.Walls = []
        self.Rooms = []
        # Longueurs
        self.MIN_ROOM = self.LEVEL.MIN_ROOM
        self.GRID_SIZE = self.LEVEL.GRID_SIZE
        self.DOOR_SIZE = self.LEVEL.DOOR_SIZE
        self.WALL_SIZE = self.MIN_ROOM // 15
        # PREDEF
        room1 = [[200, 200], [530, 200], [530, 600], [200, 600]]
        room2 = [[530, 200], [700, 200], [700, 400], [530, 400]]
        self.predef_1 = [room1, room2]
        self.LEVEL.Structures.append(self)
        self.create_building()

    def create_building(self):
        for room in self.predef_1:
            roum = Room(self)
            roum.p1 = room[0]
            roum.p2 = room[1]
            roum.p3 = room[2]
            roum.p4 = room[3]
            self.Rooms.append(roum)

    def paint_structure(self):
        for room in self.Rooms:
            room.paint_room()
        for wall in self.Walls:
            wall.paint_wall()


class Room:
    floor_texture = (168, 119, 90)
    wall_texture = (170, 160, 0)

    def __init__(self, FIREHOUSE):
        # INIT
        self.STRUCTURE = FIREHOUSE
        self.LEVEL = self.STRUCTURE.LEVEL
        self.MAIN = self.LEVEL.MAIN
        self.SCREEN = self.LEVEL.SCREEN
        self.WALL_SIZE = self.STRUCTURE.WALL_SIZE
        self.GRID_SIZE = self.STRUCTURE.GRID_SIZE
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
        self.p5 = None
        self.p6 = None
        self.polyroom = []

    def paint_room(self):
        self.poly_room()
        pygame.draw.polygon(self.SCREEN, self.floor_texture, self.polyroom)

    def poly_room(self):
        self.polyroom = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]


class Locker:

    def __init__(self, SHIFT):
        self.LEVEL = SHIFT
        self.MAIN = self.LEVEL.MAIN
        self.SCREEN = self.LEVEL.SCREEN
        self.SCREEN_RESOLUTION = self.LEVEL.SCREEN_RESOLUTION
