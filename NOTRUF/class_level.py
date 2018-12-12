from NOTRUF import class_structure, class_player, class_hose, class_firetruck, class_scba
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
    # interaction
    PICK_UP = pygame.K_SPACE
    DROP = pygame.K_g
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
        self.Vehicles = []
        self.Water = []
        self.Tools = []
        self.Burning = []
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
        # SET USEFUL POINTS
        self.STARTING_POS = [8*self.SCREEN_RESOLUTION[X]//10, 8*self.SCREEN_RESOLUTION[Y]//10]
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
        # FONTS
        self.victory_font_size = int(self.SCREEN_RESOLUTION[X] // 20)
        self.victory_font = pygame.font.SysFont('monospace', self.victory_font_size)
        self.victory_message = self.victory_font.render('Mission Accomplished', True, (0, 0, 0))
        ##############
        # FILL LEVEL #
        ##############
        self.create_structure()
        self.ignite()
        self.create_truck()
        self.intro_is_done = False
        self.intro()

    def intro(self):
        while not self.intro_is_done:
            self.Vehicles[0].arrival()
            self.update_level()
            self.paint_level()
            clock.tick(15000)
        self.create_player()

    def loop_level(self):
        self.process_input()
        self.update_level()
        self.paint_level()

        # LOCK 50 FPS
        clock.tick(50)

    def create_player(self):
        class_player.Player(self)

    def create_structure(self):
        class_structure.Structure(self)

    def create_truck(self):
        class_firetruck.Truck(self)

    def process_input(self):
        mouse_pos = pygame.mouse.get_pos()
        for unit in self.Units:
            # ROTATE_PLAYER
            unit.rotate_player(mouse_pos)
            # KEYBOARD INPUT
            key_input = pygame.key.get_pressed()
            # [DEV] FORCE QUIT LEVEL
            if key_input[self.FORCE_QUIT_LEVEL]:
                self.MAIN.create_menu()
            # PLAYER_PICK_UP
            if key_input[self.PICK_UP]:
                if unit.scba is None:
                    unit.pick_up_tool(self.Tools[1])
                elif unit.hose is None:
                    unit.pick_up_tool(self.Tools[0])
            elif key_input[self.DROP]:
                if unit.hose is not None:
                    unit.drop_hose()
                elif unit.scba is not None:
                    unit.drop_scba()
            # MOVE_PLAYER 4 DIRECTIONS
            if key_input[self.UP]:
                unit.mov_player(self.up, Y)
            elif key_input[self.DOWN]:
                unit.mov_player(self.down, Y)
            if key_input[self.RGHT]:
                unit.mov_player(self.rght, X)
            elif key_input[self.LEFT]:
                unit.mov_player(self.left, X)
            # SET_HOSE_DEBIT +/-
            if key_input[self.increase_debit]:
                unit.hose.set_hose_debit(1)
            elif key_input[self.decrease_debit]:
                unit.hose.set_hose_debit(-1)
            # MOUSE INPUT
            mouse_input = pygame.mouse.get_pressed()
            if self.Units[0].hose is not None:
                # HOSE_OPEN
                if mouse_input[0]:
                    self.Units[0].spray_baton()
                elif mouse_input[2]:
                    self.Units[0].spray_bouclier()
                elif mouse_input[1]:
                    self.Units[0].spray_medium()
                # HOSE CLOSE
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
        # STRUCTURES
        for structure in self.Structures:
            structure.paint_structure()
        # TOOLS
        for tool in self.Tools:
            if tool.__class__ is class_hose.Hose:
                tool.paint_hose()
            elif tool.__class__ is class_scba.Scba:
                tool.paint_scba()
        # WATER PARTICLES
        for water in self.Water:
            water.paint_water()
        # UNITS
        for unit in self.Units:
            unit.paint_player()
        # VEHICLES
        for truck in self.Vehicles:
            truck.paint_truck()
        # [DEV] GRID
        # self.draw_grid()
        if len(self.Burning) == 0:
            self.victory()
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

    def victory(self):
        self.SCREEN.blit(self.victory_message, (0, 0))
