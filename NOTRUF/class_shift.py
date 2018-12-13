import class_player
import pygame
clock = pygame.time.Clock()

X = 0
Y = 1

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

    def __init__(self, MAIN):
        # INIT
        self.MAIN = MAIN
        self.SCREEN = self.MAIN.SCREEN
        self.SCREEN_RESOLUTION = self.MAIN.SCREEN_RESOLUTION
        self.Units = []
        self.Structures = []
        ############
        # TEXTURES #
        ############
        self.HERBE_TEXTURE = self.MAIN.GREEN
        self.BETON_TEXTURE = self.MAIN.LIGHT_GREY
        self.BITUME_TEXTURE = self.MAIN.DARK_GREY
        # PLAYER SETTINGS
        self.PLAYER_SIZE = int(self.SCREEN_RESOLUTION[Y] // 28.4)
        self.STARTING_POS = [8*self.SCREEN_RESOLUTION[X]//10, 8*self.SCREEN_RESOLUTION[Y]//10]
        # Spawn Player
        self.create_player()

    def loop_firehouse(self):
        self.process_input()
        self.paint_shift()
        # Lock 50 FPS
        clock.tick(50)

    def paint_shift(self):
        # BACKGROUND
        self.SCREEN.fill(self.HERBE_TEXTURE)
        # UNITS
        for unit in self.Units:
            unit.paint_player()
        # Update screen
        pygame.display.flip()

    def process_input(self):
        mouse_pos = pygame.mouse.get_pos()
        for unit in self.Units:
            # ROTATE_PLAYERd
            unit.rotate_player(mouse_pos)
            # KEYBOARD INPUT
            key_input = pygame.key.get_pressed()
            # [DEV] FORCE QUIT SHIFT
            if key_input[self.FORCE_QUIT_SHIFT]:
                self.MAIN.create_menu()
            # [DEV] FORCE START LEVEL
            if key_input[self.FORCE_START_LEVEL]:
                self.MAIN.create_level()
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
        # PREDEF
        self.predef_1 = []

    def create_building(self):
        pass
