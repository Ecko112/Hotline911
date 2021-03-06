import pygame
import math
import os
import class_level

NOTRUFDir = os.path.dirname(os.path.abspath(__file__))
IMAGESDir = os.path.join(NOTRUFDir, 'IMAGES')

X = 0
Y = 1


class Player:

    def __init__(self, LEVEL):
        # INIT
        self.LEVEL = LEVEL
        self.MAIN = self.LEVEL.MAIN
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
        self.inRoom = False
        self.inDoor = True
        self.health = 300
        self.player_hitbox.center = self.pos
        self.orientation = 0
        self.prev_orientation = self.orientation
        self.p_bouteille = self.pos
        self.spraying = False
        self.checking = False
        self.hose = None
        self.scba = None
        # Set images
        self.scaled_up = int(self.SIZE * 2.75)
        self.load_images()
        self.current_image = self.Images[0]
        self.LEVEL.Units.append(self)

    def load_images(self):
        for file in ['unit_idle.png', 'unit_hose.png', 'unit_hose_scba.png', 'unit_idle_scba.png']:
            path = IMAGESDir+"/"+file
            player_png = pygame.image.load(path).convert_alpha(self.SCREEN)
            player_png = pygame.transform.scale(player_png, (self.scaled_up, self.scaled_up))
            player_png = pygame.transform.rotate(player_png, -90)
            self.Images.append(player_png)

    def paint_player(self):
        # Since a pygame texture must remain a rectangle with
        # edges parallels to the screen
        # I find a new topleft point for the surface
        # using the angle in radians
        angle = self.orientation*(math.pi/180)
        # abs(sprite_size//2*sin(x)*cos(x))
        # => = 0 if angle is a multiple of pi/2
        report = abs(self.scaled_up//2*math.sin(angle)*math.cos(angle))
        self.SCREEN.blit(self.current_image, (self.pos[X]-self.scaled_up//2-report, self.pos[Y]-self.scaled_up//2-report))

    def rotate_player(self, mouse_pos):
        # Player Sprite based on player carried equipment
        if self.hose is not None:
            if self.scba is not None:
                self.current_image = self.Images[2]
            else:
                self.current_image = self.Images[1]
        else:
            if self.scba is not None:
                self.current_image = self.Images[3]
            else:
                self.current_image = self.Images[0]

        self.prev_orientation = self.orientation
        diff_m_p = mouse_pos[X] - self.pos[X], mouse_pos[Y] - self.pos[Y]
        self.orientation = int((180/math.pi)*math.atan2(diff_m_p[Y], diff_m_p[X]))
        if self.orientation < 0:
            self.orientation += 360
        # [DEV] ROTATION PRECISION (default = 0°)
        if abs(self.orientation-self.prev_orientation) >= 0:
            self.current_image = pygame.transform.rotate(self.current_image, -self.orientation)
        else:
            self.orientation = self.prev_orientation

    def pick_up_tool(self, tool):
        if get_dist(self.pos, tool.pos) <= 30:
            tool.get_picked_up(self)

    def drop_hose(self):
        self.hose.get_dropped()
        self.hose = None

    def drop_scba(self):
        self.scba.get_dropped()
        self.scba = None

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

    def get_location(self):
        # Check wether player needs to breath from air tank
        for structure in self.LEVEL.Structures:
            for room in structure.Rooms:
                if self.player_hitbox.colliderect(room.Rect):
                    if room.temp > 40:
                        self.inRoom = True
                    if self.scba is not None:
                        self.scba.temp = str(int(room.temp))+'°'
                    return
                else:
                    if self.scba is not None:
                        self.scba.temp = 'N/A'
                        self.inRoom = False

    def get_location_vehicle(self):
        # Check wether player is near a vehicle door
        for vehicle in self.LEVEL.Vehicles:
            if self.player_hitbox.colliderect(vehicle.door):
                self.inDoor = True
                return
            else:
                self.inDoor = False

    def breath(self):
        if self.inRoom:
            if self.scba is None:
                # Hurt player
                self.health -= 0.5
            else:
                if self.scba.capacity > 0:
                    # Breath from air tank
                    self.scba.capacity -= 0.1
                else:
                    # Hurt player
                    self.health -= 0.5
            if self.health < 0:
                # Kill player
                self.die()

    def check_scba(self):
        self.checking = True

    def stop_check_scba(self):
        self.checking = False

    def leave_scene(self):
        if self.LEVEL.__class__ is class_level.Level:
            self.inDoor = False
            self.MAIN.create_shift()
        else:
            self.inDoor = False
            self.MAIN.create_level()

    def mov_player(self, direction, axe):
        self.pos[axe] += self.STEP * direction
        self.player_hitbox.center = self.pos
        # Check Wall collision
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
        # Update pos
        self.pos = [self.player_hitbox.center[X], self.player_hitbox.center[Y]]

    def die(self):
        if self.hose is not None:
            self.hose.get_dropped()
        if self.scba is not None:
            self.scba.get_dropped()
        self.LEVEL.failure()


def get_dist(point1, point2):
    return int(math.sqrt(((point1[X]-point2[X])**2)+(point1[Y]-point2[Y])**2))
