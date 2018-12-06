import pygame
# import math
pygame.font.init()

X = 0
Y= 1

class Menu:
    ################
    # KEY BINDINGS #
    ################
    # [DEV]
    # FORCE START LEVEL
    FORCE_START_LEVEL = pygame.K_BACKSPACE
    # Polices
    title_font = pygame.font.SysFont('monospace', 112, True)

    def __init__(self, MAIN):
        # INIT
        self.MAIN = MAIN
        self.SCREEN = self.MAIN.SCREEN
        self.SCREEN_RESOLUTION = self.MAIN.SCREEN_RESOLUTION
        # Set title
        self.title = self.title_font.render('HOTLINE911', True, (255, 0, 0))
        self.title_size = self.title_font.size('HOTLINE911')

    def loop_menu(self):
        self.process_input()
        self.paint_menu()

    def paint_menu(self):
        # Background
        self.SCREEN.fill((100, 100, 100))
        # Title
        self.SCREEN.blit(self.title, ((self.SCREEN_RESOLUTION[X]-self.title_size[X])//2, (self.SCREEN_RESOLUTION[Y])//4))
        # Update screen
        pygame.display.flip()

    def process_input(self):
        # KEYBOARD INPUT
        key_input = pygame.key.get_pressed()
        # [DEV] FORCE START LEVEL
        if key_input[self.FORCE_START_LEVEL]:
            self.MAIN.create_level()
