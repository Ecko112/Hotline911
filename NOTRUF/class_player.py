import pygame
import math
from NOTRUF import class_hose

X = 0
Y = 1


class Player:
    # Texture
    texture = (255, 0, 0)

    def __init__(self, LEVEL):
        # INIT
        self.LEVEL = LEVEL
        self.MAIN = self.LEVEL
        self.SCREEN = self.LEVEL.SCREEN
        self.Images = []
        ###################
        # PLAYER SETTINGS #
        ###################
        self.SIZE = int(self.LEVEL.PLAYER_SIZE)
        self.STEP = int(self.SIZE / 7)
        self.player_hitbox = pygame.Rect(0, 0, self.SIZE*2, self.SIZE*2)
        # Set spawn default status
        self.pos = [int(self.LEVEL.STARTING_POS[X]), int(self.LEVEL.STARTING_POS[Y])]
        self.player_hitbox.center = self.pos
        self.orientation = 0
        self.p_bouteille = self.pos
        self.spraying = False
        # Set images
        self.load_images()
        self.current_image = self.Images[0]
        # [DEV] Start with Hose
        self.hose = class_hose.Hose(self)

    def load_images(self):
        for file in ('unit_att_UP.png', 'unit_att_RGHT.png', 'unit_att_DOWN.png', 'unit_att_LEFT.png'):
            path = '/home/louis/Documents/Universite/INFO2056/notruf112/UNDER_PROGRESS/IMAGES/' + file
            player_png = pygame.image.load(path).convert_alpha(self.SCREEN)
            player_png_0 = pygame.transform.scale(player_png, (self.SIZE * 6 // 2, self.SIZE * 6 // 2))
            player_png_0 = pygame.transform.rotate(player_png_0, -90)
            self.Images.append(player_png_0)

    def paint_player(self):
        # pygame.draw.circle(self.SCREEN, self.texture, self.pos, self.SIZE)
        # pygame.draw.circle(self.SCREEN, (100, 100, 100), self.p_bouteille, 15)
        self.SCREEN.blit(self.current_image, (self.pos[X]-self.SIZE*6//4, self.pos[Y]-self.SIZE*6//4))

    def rotate_player(self, mouse_pos):
        diff_m_p = mouse_pos[X] - self.pos[X], mouse_pos[Y] - self.pos[Y]
        self.orientation = (180/math.pi)*math.atan2(diff_m_p[Y], diff_m_p[X])
        if self.orientation < 0:
            self.orientation += 360
        self.current_image = pygame.transform.rotate(self.Images[0], -self.orientation)
        # self.p_bouteille = (int(self.pos[X]+10*math.cos(self.orientation + math.pi)), int(self.pos[Y]+10*math.sin(self.orientation + math.pi)))

    def spray(self):
        self.hose.spray_water(self)

    def stop_spray(self):
        self.spraying = False

    def mov_player(self, direction, axe):
        self.pos[axe] += self.STEP * direction
        self.player_hitbox.center = self.pos
        for structure in self.LEVEL.Structures:
            for wall in structure.Walls:
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
