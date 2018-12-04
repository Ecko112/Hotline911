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
    # INPUT
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

    def __init__(self, name, screen_resolution, MAIN):
        self.NAME = name
        self.ZONE = [screen_resolution[X]//1.1234, screen_resolution[Y]//1.424]
        self.PLAYER_SIZE = screen_resolution[Y]//28.4
        self.STARTING_POS = (self.ZONE[X] - self.ZONE[X]//10, self.ZONE[Y] + 1*self.ZONE[Y]//10 + self.PLAYER_SIZE + 10)
        self.MIN_ROOM = self.PLAYER_SIZE*6
        self.DOOR_SIZE = self.PLAYER_SIZE*3-10
        self.ZONE[X] = self.ZONE[X] - self.ZONE[X]%self.MIN_ROOM
        self.ZONE[Y] = self.ZONE[Y] - self.ZONE[Y]%self.MIN_ROOM
        self.UPPER_LEFT = (screen_resolution[X]//18.21, 5)
        self.LOWER_RGHT = (self.UPPER_LEFT[X]+self.ZONE[X], self.UPPER_LEFT[Y]+self.ZONE[Y])
        self.ROUTEH = (0, self.ZONE[Y] + 1*self.ZONE[Y]//10)
        self.SCREEN_RESOLUTION = screen_resolution
        self.MAIN = MAIN
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
        screen.fill(self.HERBE_TEXTURE)
        pygame.draw.rect(screen, self.BITUME_TEXTURE, (self.ROUTEH, (self.SCREEN_RESOLUTION[X], self.SCREEN_RESOLUTION[Y] - self.ROUTEH[Y])))
        pygame.draw.rect(screen, self.PLAYER_TEXTURE, ((self.STARTING_POS[X]-300, self.STARTING_POS[Y]), (400, self.SCREEN_RESOLUTION[Y])))

        for structure in self.Structures:
            class_structure.Structure.paint_structure(structure, screen)
        for unit in self.Units:
            class_player.Player.paint_player(unit, screen)
        # self.draw_grid(screen)

    def process_input(self):
        mouse_pos = pygame.mouse.get_pos()
        for unit in self.Units:
            class_player.Player.rotate_player(unit, mouse_pos)
            input = pygame.key.get_pressed()
            if input[self.UP]:
                class_player.Player.mov_player(self.Units[0], self.up, Y)
            elif input[self.DOWN]:
                class_player.Player.mov_player(self.Units[0], self.down, Y)
            if input[self.RGHT]:
                class_player.Player.mov_player(self.Units[0], self.rght, X)
            elif input[self.LEFT]:
                class_player.Player.mov_player(self.Units[0], self.left, X)
            if input[self.increase_debit]:
                self.Units[0].hose.set_hose_debit(1)
            elif input[self.decrease_debit]:
                self.Units[0].hose.set_hose_debit(-1)
            if input[self.increase_spray]:
                self.Units[0].hose.set_hose_spray(1)
            elif input[self.decrease_spray]:
                self.Units[0].hose.set_hose_spray(-1)

            click = pygame.mouse.get_pressed()

            if click[0]:
                class_player.Player.spray(self.Units[0])
            if not click[0]:
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
