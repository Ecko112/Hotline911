import pygame
import sys
from NOTRUF import class_level, class_menu, class_firehouse

X = 0
Y = 1


class Main:
    # Game Stages
    User_Stage = None
    Stages = ["inMenu", "inLevel", "inFirehouse"]
    # Level
    Level = None
    # Station
    Firehouse = None
    # Menu
    Menu = None
    ##########
    # COLORS #
    ##########
    RED = (255, 0, 0)
    GREEN = (0, 153, 0)
    LIGHT_GREY = (169, 169, 169)
    DARK_GREY = (32, 32, 32)

    def __init__(self, screen_resolution):
        # Set SCREEN_RESOLUTION while keeping ratio
        self.SCREEN_RESOLUTION = [0, 0]
        self.SCREEN_RESOLUTION[X] = screen_resolution[X]
        self.SCREEN_RESOLUTION[Y] = int(self.SCREEN_RESOLUTION[X]/1.9158)
        # Set PYGAME screen
        self.SCREEN = pygame.display.set_mode(self.SCREEN_RESOLUTION)
        pygame.display.set_caption('Hotline 911')

    def create_level(self):
        self.User_Stage = self.Stages[1]
        self.Level = class_level.Level(self)
        self.delete_menu()
        self.delete_firehouse()

    def delete_level(self):
        self.Level = None

    def create_menu(self):
        self.User_Stage = self.Stages[0]
        self.Menu = class_menu.Menu(self)
        self.delete_level()
        self.delete_firehouse()

    def delete_menu(self):
        self.Menu = None

    def create_firehouse(self):
        self.User_Stage = self.Stages[2]
        self.Firehouse = class_firehouse.Firehouse(self)
        self.delete_level()
        self.delete_menu()

    def delete_firehouse(self):
        self.Firehouse = None

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()

    def exit_game(self):
        # Could be static
        # but easier to call from other classes
        # when referring to self.MAIN
        pygame.quit()
        sys.exit()

    def loop_main(self):
        self.process_input()
        if self.User_Stage is 'inMenu':
            self.Menu.loop_menu()
        elif self.User_Stage is 'inLevel':
            self.Level.loop_level()
        elif self.User_Stage is 'inFirehouse':
            self.Firehouse.loop_firehouse()
