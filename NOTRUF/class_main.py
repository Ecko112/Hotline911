import pygame
from NOTRUF import class_level
from NOTRUF import class_menu

X = 0
Y = 1


class Main:
    # Game Stages
    User_Stage = None
    Stages = ["inMenu", "inLevel"]
    # Level
    Level = None
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
        self.update_user_stage('goLevel')
        self.Level = class_level.Level(self)

    def delete_level(self):
        self.update_user_stage('goMenu')
        self.Level = None

    def create_menu(self):
        self.update_user_stage('goMenu')
        self.Menu = class_menu.Menu(self)

    def delete_menu(self):
        self.update_user_stage('goLevel')
        self.Menu = None

    def update_user_stage(self, new_stage):
        if new_stage is 'goMenu':
            self.User_Stage = self.Stages[0]
        elif new_stage is 'goLevel':
            self.User_Stage = self.Stages[1]
        else:
            print('MOVING USER STAGE : ERROR')

    def loop_main(self):
        print(self.User_Stage)
        print('avocado')
        if self.User_Stage is 'inMenu':
            self.Menu.loop_menu()
        elif self.User_Stage is 'inLevel':
            self.Level.loop_level()
