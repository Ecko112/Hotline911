import pygame
import sys
from UNDER_PROGRESS import tests as t

X = 0
Y = 1

screen = pygame.display.set_mode((1377, 713))

unit = t.Unit(screen)
hose = t.Hose(unit)


def deal_w_input():
    input = pygame.key.get_pressed()
    if input[pygame.K_z]:
        t.Unit.mov_player(unit, -1, Y)
    elif input[pygame.K_s]:
        t.Unit.mov_player(unit, 1, Y)
    if input[pygame.K_d]:
        t.Unit.mov_player(unit, 1, X)
    elif input[pygame.K_q]:
        t.Unit.mov_player(unit, -1, X)


pygame.init()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    deal_w_input()
    screen.fill((100, 100, 100))
    unit.paint_player()
    unit.hose.paint_hose()

    pygame.display.flip()
    clock.tick(50)
