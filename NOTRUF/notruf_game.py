# IMPORTS
import pygame
from NOTRUF import class_main

# SETTINGS
# SCREEN_RESOLUTION = (1366, 713)
SCREEN_RESOLUTION = (1280, 713)
#################
# PYGAME.INIT() #
#################
pygame.init()
# CREATE_MAIN_CLASS
main = class_main.Main(SCREEN_RESOLUTION)
main.create_menu()
#################
#   MAIN LOOP   #
#################
while True:
    main.loop_main()
#################
