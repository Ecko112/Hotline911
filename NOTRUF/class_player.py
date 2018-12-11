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
        self.prev_orientation = self.orientation
        self.p_bouteille = self.pos
        self.spraying = False
        # Set images
        self.scaled_up = 2.75
        self.scaled_up *= self.SIZE
        self.scaled_up = int(self.scaled_up)
        self.load_images()
        self.current_image = self.Images[0]
        # [DEV] Start with Hose
        self.hose = class_hose.Hose(self)

    def load_images(self):
        for file in ['unit.png']:
            path = '/home/louis/Documents/Universite/INFO2056/notruf112/UNDER_PROGRESS/IMAGES/' + file
            player_png = pygame.image.load(path).convert_alpha(self.SCREEN)
            player_png_0 = pygame.transform.scale(player_png, (self.scaled_up, self.scaled_up))
            player_png_0 = pygame.transform.rotate(player_png_0, -90)
            self.Images.append(player_png_0)

    def paint_player(self):
        angle = self.orientation*(math.pi/180)
        report = abs(self.scaled_up//2*math.sin(angle)*math.cos(angle))
        self.SCREEN.blit(self.current_image, (self.pos[X]-self.scaled_up//2-report, self.pos[Y]-self.scaled_up//2-report))

    def rotate_player(self, mouse_pos):
        self.prev_orientation = self.orientation
        diff_m_p = mouse_pos[X] - self.pos[X], mouse_pos[Y] - self.pos[Y]
        self.orientation = int((180/math.pi)*math.atan2(diff_m_p[Y], diff_m_p[X]))
        if self.orientation < 0:
            self.orientation += 360
        # [DEV] ROTATION PRECISION
        if abs(self.orientation-self.prev_orientation) >= 0:
            self.current_image = pygame.transform.rotate(self.Images[0], -self.orientation)
        else:
            self.orientation = self.prev_orientation

    def spray_baton(self):
        self.hose.set_hose_spray(0)
        self.hose.spray_water()

    def spray_medium(self):
        self.hose.set_hose_spray(1)
        self.hose.spray_water()

    def spray_bouclier(self):
        self.hose.set_hose_spray(2)
        self.hose.spray_water()

    def spray_stop(self):
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
