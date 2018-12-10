from NOTRUF import class_structure, class_player
import pygame
import random

pygame.init()
clock = pygame.time.Clock()

X = 0
Y = 1


class Level:
    ################
    # KEY BINDINGS #
    ################
    # [DEV]
    # FORCE QUIT LEVEL
    FORCE_QUIT_LEVEL = pygame.K_DELETE
    # Player
    UP = pygame.K_z
    DOWN = pygame.K_s
    LEFT = pygame.K_q
    RGHT = pygame.K_d
    up = left = -1
    down = rght = 1
    # Hose
    increase_debit = pygame.K_a
    decrease_debit = pygame.K_e

    def __init__(self, MAIN):
        # INIT
        self.MAIN = MAIN
        self.SCREEN_RESOLUTION = self.MAIN.SCREEN_RESOLUTION
        self.SCREEN = self.MAIN.SCREEN
        # Lists
        self.Structures = []
        self.Units = []
        self.Water = []
        # PLAYER SETTINGS
        self.PLAYER_SIZE = int(self.SCREEN_RESOLUTION[Y]//28.4)
        # STRUCTURE SETTINGS
        self.MIN_ROOM = self.PLAYER_SIZE * 6
        self.DOOR_SIZE = self.PLAYER_SIZE * 3 - 10
        # BUILDABLE ZONE
        self.ZONE = [self.SCREEN_RESOLUTION[X]//1.1234, self.SCREEN_RESOLUTION[Y]//1.424]
        #
        self.ZONE[X] -= self.ZONE[X] % self.MIN_ROOM
        self.ZONE[Y] -= self.ZONE[Y] % self.MIN_ROOM
        # PLAYER SETTINGS
        self.STARTING_POS = (self.ZONE[X] - self.ZONE[X]//10, self.ZONE[Y] + 1*self.ZONE[Y]//10 + self.PLAYER_SIZE + 10)
        # SET USEFUL POINTS
        self.UPPER_LEFT = (self.SCREEN_RESOLUTION[X]//18.21, 5)
        self.LOWER_RGHT = (self.UPPER_LEFT[X]+self.ZONE[X], self.UPPER_LEFT[Y]+self.ZONE[Y])
        self.ROUTEH = (0, 11*self.ZONE[Y]//10)
        # OTHER
        self.GRID_SIZE = self.MIN_ROOM//6
        ############
        # TEXTURES #
        ############
        self.PLAYER_TEXTURE = self.MAIN.RED
        self.HERBE_TEXTURE = self.MAIN.GREEN
        self.BETON_TEXTURE = self.MAIN.LIGHT_GREY
        self.BITUME_TEXTURE = self.MAIN.DARK_GREY
        ##############
        # FILL LEVEL #
        ##############
        self.create_structure()
        self.create_player()
        self.ignite()

    def loop_level(self):
        self.process_input()
        self.update_level()
        self.paint_level()
        # LOCK 50 FPS
        clock.tick(50)

    def create_player(self):
        player = class_player.Player(self)
        self.Units.append(player)

    def create_structure(self):
        # Create
        structure = class_structure.Structure(self)
        self.Structures.append(structure)

    def process_input(self):
        mouse_pos = pygame.mouse.get_pos()
        for unit in self.Units:
            # ROTATE_PLAYER
            class_player.Player.rotate_player(unit, mouse_pos)
            # KEYBOARD INPUT
            key_input = pygame.key.get_pressed()
            # [DEV] FORCE QUIT LEVEL
            if key_input[self.FORCE_QUIT_LEVEL]:
                self.MAIN.create_menu()
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
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.Units[0].hose.set_hose_debit(1)
                    elif event.button == 5:
                        self.Units[0].hose.set_hose_debit(-1)

            # MOUSE INPUT
            mouse_input = pygame.mouse.get_pressed()
            # HOSE_OPEN/CLOSE
            if mouse_input[0]:
                self.Units[0].spray_baton()
            elif mouse_input[2]:
                self.Units[0].spray_bouclier()
            elif mouse_input[1]:
                self.Units[0].spray_medium()
            else:
                self.Units[0].spray_stop()

    def ignite(self):
        self.Structures[random.randint(0, len(self.Structures)-1)].ignite()

    def update_level(self):
        for structure in self.Structures:
            structure.burn()
        for water in self.Water:
            water.move_water()

    def paint_level(self):
        # BACKGROUND
        self.SCREEN.fill(self.HERBE_TEXTURE)
        pygame.draw.rect(self.SCREEN, self.BITUME_TEXTURE, (self.ROUTEH, (self.SCREEN_RESOLUTION[X], self.SCREEN_RESOLUTION[Y] - self.ROUTEH[Y])))
        # VEHICLES
        pygame.draw.rect(self.SCREEN, (255, 10, 20), ((self.STARTING_POS[X]-300, self.STARTING_POS[Y]), (400, self.SCREEN_RESOLUTION[Y])))
        # STRUCTURES
        for structure in self.Structures:
            class_structure.Structure.paint_structure(structure)
        # WATER PARTICLES
        for water in self.Water:
            water.paint_water()
        # UNITS
        for unit in self.Units:
            unit.paint_player()
        # [DEV] GRID
        self.draw_grid()
        # Update screen
        pygame.display.flip()

    def draw_grid(self):
        report = [self.UPPER_LEFT[X], self.UPPER_LEFT[Y]]
        while report[Y] < self.LOWER_RGHT[Y]:
            while report[X] < self.LOWER_RGHT[X]:
                rect = pygame.Rect(report[X], report[Y], self.MIN_ROOM//6, self.MIN_ROOM//6)
                pygame.draw.rect(self.SCREEN, (100, 100, 100), rect, 1)
                report[X] += self.MIN_ROOM//6
            report[Y] += self.MIN_ROOM//6
            report[X] = self.UPPER_LEFT[X]
