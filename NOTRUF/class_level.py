from NOTRUF import class_structure, class_player
import pygame

X = 0
Y = 1


class Level:
    # Lists
    Zones = []
    Structures = []
    Units = []
    # Booleans
    add_one_structure = True
    # Colors
    RED = (255, 0, 0)
    GREEN = (0, 153, 0)
    LIGHT_GREY = (169, 169, 169)
    DARK_GREY = (32, 32, 32)
    # KEY BINDINGS
    # Player
    UP = pygame.K_z
    DOWN = pygame.K_s
    LEFT = pygame.K_q
    RGHT = pygame.K_d
    up = left = -1
    down = rght = 1
    # Hose
    increase_spray = pygame.K_UP
    decrease_spray = pygame.K_DOWN
    increase_debit = pygame.K_RIGHT
    decrease_debit = pygame.K_LEFT

    def __init__(self, MAIN):
        # INIT
        self.MAIN = MAIN
        self.SCREEN_RESOLUTION = self.MAIN.SCREEN_RESOLUTION
        self.SCREEN = self.MAIN.SCREEN
        # BUILDABLE ZONE
        self.ZONE = [self.SCREEN_RESOLUTION[X]//1.1234, self.SCREEN_RESOLUTION[Y]//1.424]
        self.PLAYER_SIZE = screen_resolution[Y]//28.4
        self.STARTING_POS = (self.ZONE[X] - self.ZONE[X]//10, self.ZONE[Y] + 1*self.ZONE[Y]//10 + self.PLAYER_SIZE + 10)
        self.MIN_ROOM = self.PLAYER_SIZE*6
        self.DOOR_SIZE = self.PLAYER_SIZE*3-10
        self.ZONE[X] = self.ZONE[X] - self.ZONE[X]%self.MIN_ROOM
        self.ZONE[Y] = self.ZONE[Y] - self.ZONE[Y]%self.MIN_ROOM
        self.UPPER_LEFT = (screen_resolution[X]//18.21, 5)
        self.LOWER_RGHT = (self.UPPER_LEFT[X]+self.ZONE[X], self.UPPER_LEFT[Y]+self.ZONE[Y])
        self.ROUTEH = (0, self.ZONE[Y] + 1*self.ZONE[Y]//10)
        # Textures
        self.PLAYER_TEXTURE = self.RED
        self.HERBE_TEXTURE = self.GREEN
        self.BETON_TEXTURE = self.LIGHT_GREY
        self.BITUME_TEXTURE = self.DARK_GREY

        self.create_structure()
        self.create_player()

    def create_player(self):
        player = class_player.Player(self.STARTING_POS[X], self.STARTING_POS[Y], self.PLAYER_SIZE, self.MAIN, self)
        self.add_unit(player)

    def add_unit(self, unit):
        self.Units.append(unit)

    def create_structure(self):
        i = 1
        while self.add_one_structure:

            structure = class_structure.Structure('structure_'+str(i), self.MAIN, self)

            self.add_structure(structure)
            self.add_one_structure = False

    def add_structure(self, structure):
        self.Structures.append(structure)

    def paint_level(self, screen):
        # BACKGROUND
        screen.fill(self.HERBE_TEXTURE)
        pygame.draw.rect(screen, self.BITUME_TEXTURE, (self.ROUTEH, (self.SCREEN_RESOLUTION[X], self.SCREEN_RESOLUTION[Y] - self.ROUTEH[Y])))
        # VEHICLES
        pygame.draw.rect(screen, (255, 10, 20), ((self.STARTING_POS[X]-300, self.STARTING_POS[Y]), (400, self.SCREEN_RESOLUTION[Y])))
        # STRUCTURES
        for structure in self.Structures:
            class_structure.Structure.paint_structure(structure, screen)
        # UNITS
        for unit in self.Units:
            class_player.Player.paint_player(unit, screen)
        # [DEV] GRID
        # self.draw_grid(screen)

    def process_input(self):
        mouse_pos = pygame.mouse.get_pos()
        for unit in self.Units:
            # ROTATE_PLAYER
            class_player.Player.rotate_player(unit, mouse_pos)
            # KEYBOARD INPUT
            key_input = pygame.key.get_pressed()
            # MOVE_PLAYER 4 DIRECTIONS
            if key_input[self.UP]:
                class_player.Player.mov_player(self.Units[0], self.up, Y)
            elif key_input[self.DOWN]:
                class_player.Player.mov_player(self.Units[0], self.down, Y)
            if key_input[self.RGHT]:
                class_player.Player.mov_player(self.Units[0], self.rght, X)
            elif key_input[self.LEFT]:
                class_player.Player.mov_player(self.Units[0], self.left, X)
            # SET_HOSE_DEBIT +/-
            if key_input[self.increase_debit]:
                self.Units[0].hose.set_hose_debit(1)
            elif key_input[self.decrease_debit]:
                self.Units[0].hose.set_hose_debit(-1)
            # SET_HOSE_ANGLE +/-
            if key_input[self.increase_spray]:
                self.Units[0].hose.set_hose_spray(1)
            elif key_input[self.decrease_spray]:
                self.Units[0].hose.set_hose_spray(-1)
            # MOUSE INPUT
            mouse_input = pygame.mouse.get_pressed()
            # HOSE_OPEN/CLOSE
            if mouse_input[0]:
                class_player.Player.spray(self.Units[0])
            if not mouse_input[0]:
                class_player.Player.stop_spray(self.Units[0])

    def draw_grid(self, screen):
        report = [self.UPPER_LEFT[X], self.UPPER_LEFT[Y]]
        while report[Y] < self.LOWER_RGHT[Y]:
            while report[X] < self.LOWER_RGHT[X]:
                rect = pygame.Rect(report[X], report[Y], self.MIN_ROOM//6, self.MIN_ROOM//6)
                pygame.draw.rect(screen, (100, 100, 100), rect, 1)
                report[X] += self.MIN_ROOM//6
            report[Y] += self.MIN_ROOM//6
            report[X] = self.UPPER_LEFT[X]
