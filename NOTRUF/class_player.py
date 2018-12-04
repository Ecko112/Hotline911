import pygame
import math
from NOTRUF import class_hose

X = 0
Y = 1


class Player:
    # Texture
    texture = (255, 0, 0)
    # Init
    pos = []
    last_pos = []
    next_pos = []
    SIZE = 0
    rect = None
    in_door = False
    k = 1

    def __init__(self, pos_x, pos_y, size, MAIN, LEVEL):
        # INIT
        self.MAIN = MAIN
        self.LEVEL = LEVEL
        self.pos = [int(pos_x), int(pos_y)]
        self.last_pos = self.pos
        self.SIZE = int(size)
        self.step = int(size/7)
        self.player_hitbox = pygame.Rect(0, 0, self.SIZE*2, self.SIZE*2)
        self.player_hitbox.center = self.pos
        self.orientation = 0
        self.p_bouteille = self.pos
        self.watercone = []
        self.spraying = False
        self.hose = class_hose.Hose()

    def paint_player(self, screen):
        pygame.draw.circle(screen, self.texture, self.pos, self.SIZE)
        pygame.draw.circle(screen, (100, 100, 100), self.p_bouteille, 15)
        # if self.spraying:
            # pygame.draw.polygon(screen, (42, 164, 201), self.hose.watercone)
            # pygame.draw.aalines(screen, (100, 0, 0), True, self.hose.watercone, 1)
            # pygame.draw.rect(screen, (150, 0, 0), self.hose.waterfront, 1)
        for water in self.hose.water:
            water.move_water()

    def rotate_player(self, mouse_pos):
        diff_m_p = mouse_pos[X] - self.pos[X], mouse_pos[Y] - self.pos[Y]
        self.orientation = math.atan2(diff_m_p[Y], diff_m_p[X])
        self.p_bouteille = (int(self.pos[X]+10*math.cos(self.orientation + math.pi)), int(self.pos[Y]+10*math.sin(self.orientation + math.pi)))

    def spray(self):
        class_hose.Hose.spray_water(self.hose, self)

    def stop_spray(self):
        self.spraying = False

    def mov_player(self, direction, axe):
        self.pos[axe] += self.step * direction
        self.player_hitbox.center = self.pos
        j = 1
        for structure in self.LEVEL.Structures:
            j += 1
            k = 1
            for wall in structure.Walls:
                k += 1
                if self.player_hitbox.colliderect(wall.Rect):
                    if axe == X:
                        if direction == -1:
                            self.player_hitbox.left = wall.Rect.right
                        elif direction == 1:
                            self.player_hitbox.right = wall.Rect.left
                    elif axe == Y:
                        if direction == -1:
                            self.player_hitbox.top = wall.Rect.bottom
                        elif direction == 1:
                            self.player_hitbox.bottom = wall.Rect.top

        self.pos = [self.player_hitbox.center[X], self.player_hitbox.center[Y]]

