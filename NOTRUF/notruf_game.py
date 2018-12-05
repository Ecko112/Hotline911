# IMPORTS
import pygame
import sys
from NOTRUF import class_main

# SETTINGS
SCREEN_RESOLUTION = (1366, 713)


# LEAVE MAIN LOOP
def process_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


#################
# PYGAME.INIT() #
#################
pygame.init()
clock = pygame.time.Clock()

# CREATE_MAIN_CLASS
main = class_main.Main(SCREEN_RESOLUTION)
main.create_menu()
#############
# MAIN LOOP #
#############

while True:
    process_input()
    main.loop_main()

    # AIM FOR 50 FPS
    clock.tick(50)
