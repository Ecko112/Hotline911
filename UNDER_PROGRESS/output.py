import pygame
from NOTRUF import class_main
from NOTRUF import class_level


X = 0
Y = 1

# pygame.init()
clock = pygame.time.Clock()

main = class_main.Main()

main.create_level()

for wall in main.Levels[0].Structures[0].Walls:
    print(wall.name)
while True:
    main.process_input()
    main.game_display()
    clock.tick(50)
