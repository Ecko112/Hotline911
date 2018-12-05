# IMPORTS
import pygame
from NOTRUF import class_main

# SETTINGS
SCREEN_RESOLUTION = (1366, 713)
#################
# PYGAME.INIT() #
#################
pygame.init()
clock = pygame.time.Clock()

# CREATE_MAIN_CLASS
main = class_main.Main(SCREEN_RESOLUTION)

#############
# MAIN LOOP #
#############

while True:
    main.process_input()
    main.game_display()

    # AIM FOR 50 FPS
    clock.tick(50)
