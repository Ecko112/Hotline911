import pygame
import sys
from NOTRUF import class_level

X = 0
Y = 1


class Main:
    # Lists
    Levels = []
    # Booleans
    add_one_level = True
    # Cstes
    SCREEN_RESOLUTION = (1366, 713)

    def __init__(self):
        self.screen = pygame.display.set_mode(self.SCREEN_RESOLUTION)
        pygame.display.set_caption('Hotline 911')

    def create_level(self):
        i = 1
        while self.add_one_level:
            level = class_level.Level('level_' + str(i), self.SCREEN_RESOLUTION, self)
            self.add_level(level)
            self.add_one_level = False

    def add_level(self, level):
        self.Levels.append(level)

    def game_display(self):
        for level in self.Levels:
            class_level.Level.paint_level(level, self.screen)

        pygame.display.flip()

    def process_input(self):
        pygame.key.set_repeat()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for level in self.Levels:
            class_level.Level.process_input(level)

