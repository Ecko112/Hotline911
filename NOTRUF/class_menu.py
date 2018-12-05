import pygame
import math


class Menu:
    ################
    # KEY BINDINGS #
    ################
    FORCE_START_LEVEL = pygame.K_BACKSPACE

    def __init__(self, MAIN):
        # INIT
        self.MAIN = MAIN
        self.SCREEN = self.MAIN.SCREEN

    def paint_menu(self):
        self.SCREEN.fill((100, 100, 100))

    def process_input(self):
        # KEYBOARD INPUT
        key_input = pygame.key.get_pressed()
        # [DEV] MANUALLY START LEVEL
        if key_input[self.FORCE_START_LEVEL]:
            self.MAIN.create_level()

    def loop_menu(self):
        self.process_input()
        self.paint_menu()
