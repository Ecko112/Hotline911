import pygame
import math


class Menu:

    def __init__(self, main):
        # INIT
        self.MAIN = main
        self.SCREEN = self.MAIN.SCREEN

    def paint_menu(self):
        self.SCREEN.fill((100, 100, 100))
