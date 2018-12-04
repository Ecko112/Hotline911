import pygame
from NOTRUF import class_main


X = 0
Y = 1

pygame.init()
clock = pygame.time.Clock()

main = class_main.Main()

# main.create_level()

# main.Levels[0].Structures[0].ignite()

while True:
    main.process_input()
    if main.inLevel:
        main.Levels[0].Structures[0].burn()

    main.game_display()
    clock.tick(50)
