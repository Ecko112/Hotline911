# IMPORTS
import pygame
import sys
from NOTRUF import class_main

# SETTINGS
SCREEN_RESOLUTION = (1366, 713)

FPS = 50

#################
# PYGAME.INIT() #
#################
pygame.init()
clock = pygame.time.Clock()

# CREATE_MAIN_CLASS
main = class_main.Main(SCREEN_RESOLUTION)
main.create_menu()
#################
#   MAIN LOOP   #
#################
while True:
    main.loop_main()

    # LOCK FPS
    clock.tick(FPS)
#############
