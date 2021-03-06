import pygame
import math

X = 0
Y = 1


class Unit:
    pos = [200, 200]
    size = 23
    hose = None

    def __init__(self, screen):
        self.screen = screen

    def mov_player(self, direction, axe):
        self.pos[axe] += 3*direction
        self.hose.set_hose_line()

    def paint_player(self):
        pygame.draw.circle(self.screen, (32, 32, 32), self.pos, self.size)


class Hose:
    texture = (206, 5, 5)
    hose_line = [[200, 200], [200, 200]]
    polyhose = []

    def __init__(self, unit):
        self.handler = unit
        self.screen = self.handler.screen
        self.spawn = self.handler.pos
        # self.hose_line.append(self.spawn)
        self.handler.hose = self

    def paint_hose(self):
        pygame.draw.lines(self.screen, self.texture, False, self.hose_line, 10)

    def set_hose_line(self):
        self.hose_line[-1] = self.handler.pos
        dist = get_dist(self.handler.pos, self.hose_line[-2])
        if dist > 75:
            self.hose_line.insert(-1, self.handler.pos[:])
        elif len(self.hose_line) > 3 and get_dist(self.handler.pos, self.hose_line[-3]) < 100:
            self.hose_line.pop(-2)

    def set_2_point(self):
        for point in self.hose_line:
            pass

    def set_poly_hose(self):
            pass


def get_dist(point1, point2):
    return int(math.sqrt(((point1[X]-point2[X])**2)+(point1[Y]-point2[Y])**2))


def get_angle(point1, point2):
    return math.atan2(point2[Y]-point1[Y], point2[X]-point1[X])
