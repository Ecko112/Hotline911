import pygame
# import math
pygame.font.init()

X = 0
Y = 1


class Menu:
    ################
    # KEY BINDINGS #
    ################
    # [DEV]
    # FORCE START LEVEL
    FORCE_START_LEVEL = pygame.K_BACKSPACE
    # Polices

    def __init__(self, MAIN):
        # INIT
        self.MAIN = MAIN
        self.SCREEN = self.MAIN.SCREEN
        self.SCREEN_RESOLUTION = self.MAIN.SCREEN_RESOLUTION
        # Set Logo
        self.logo_size = (int(self.SCREEN_RESOLUTION[X]//2.61), int(self.SCREEN_RESOLUTION[X]//11.87))
        self.logo_pos = [0, 0]
        self.logo_png = pygame.image.load('/home/louis/Documents/Universite/INFO2056/notruf112/NOTRUF/IMAGES/logo.png').convert_alpha(self.SCREEN)
        self.logo_png = pygame.transform.scale(self.logo_png, self.logo_size)

        # Set Exit Game
        self.exit_game_font_size = int(self.SCREEN_RESOLUTION[X]//39.02)
        self.exit_game_font = pygame.font.SysFont('monospace', self.exit_game_font_size)
        self.exit_game = Button("Exit Game", self.exit_game_font, (255, 255, 255), (255, 0, 0), self)
        self.exit_game.pos = [(self.SCREEN_RESOLUTION[X]-self.exit_game.size[X])//2, 8*self.SCREEN_RESOLUTION[Y]//10]

    def loop_menu(self):
        self.process_input()
        self.paint_menu()

    def paint_menu(self):
        # Background
        self.SCREEN.fill((100, 100, 100))
        # Logo
        self.SCREEN.blit(self.logo_png, self.logo_pos)
        # Buttons
        # Exit
        self.exit_game.paint_button()
        # Update screen
        pygame.display.flip()

    def process_input(self):
        # KEYBOARD INPUT
        key_input = pygame.key.get_pressed()
        # [DEV] FORCE START LEVEL
        if key_input[self.FORCE_START_LEVEL]:
            self.MAIN.create_level()


class Button:

    def __init__(self, text, font, font_color, back_color, MENU):
        # INIT
        self.MENU = MENU
        self.MAIN = self.MENU.MAIN
        self.SCREEN = self.MENU.SCREEN
        self.pos = [0, 0]
        # Set Text
        self.text = text
        self.font = font
        self.font_color = font_color
        self.back_color = back_color
        self.size = self.font.size(self.text)
        # Create Surface
        self.title = self.font.render(text, True, self.font_color, self.back_color)

    def paint_button(self):
        self.SCREEN.blit(self.title, self.pos)

