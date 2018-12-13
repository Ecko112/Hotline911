import pygame

pygame.font.init()

X = 0
Y = 1

t = 0


class Furniture:
    texture = (200, 200, 150)

    ignition_tresh = 80

    def __init__(self, pos, length, width, ROOM):
        # INIT
        self.ROOM = ROOM
        self.SCREEN = self.ROOM.SCREEN
        self.STRUCTURE = self.ROOM.STRUCTURE
        self.LEVEL = self.ROOM.LEVEL
        self.MAIN = self.ROOM.LEVEL
        self.burning = False

        # SETTINGS
        self.pos = pos
        self.length = length
        self.width = width
        self.area = self.length*self.width
        self.health = self.area
        self.grid_area = int(self.area/(self.ROOM.GRID_SIZE**2))
        self.Rect = self.influence_Rect = pygame.Rect(0, 0, self.length, self.width)
        self.Rect.center = self.influence_Rect.center = self.pos
        # Check collision
        collision = False
        for wall in self.STRUCTURE.Walls:
            if self.Rect.colliderect(wall.Rect):
                collision = True
        if not collision:
            for furniture in self.STRUCTURE.Furniture:
                if self.Rect.colliderect(furniture.Rect):
                    collision = True
        # Attributes
        # Radiation Rectangle
        self.influence_rad = 0
        self.influence_rad_max = self.STRUCTURE.GRID_SIZE * 3
        self.influence = 1/100
        self.influence_room = self.influence
        # Ignitability
        self.temp = self.ROOM.temp
        self.wetness = 0
        # Save Self
        if not collision:
            self.ROOM.Furniture.append(self)
            self.STRUCTURE.Furniture.append(self)
        # OTHER
        self.temp_font_size = 20
        self.temp_font = pygame.font.SysFont('monospace', self.temp_font_size)
        self.temp_message = self.temp_font.render(str(self.temp), False, (0, 0, 0))

    def paint_furniture(self):
        pygame.draw.rect(self.SCREEN, self.texture, self.Rect)
        # [DEV] DRAW RADIATION ZONE
        pygame.draw.rect(self.SCREEN, (0, 0, 0), self.influence_Rect, 2)
        # [DEV] BLIT TEMPERATURE
        global t
        if t == 10:
            self.temp_message = self.temp_font.render(str(self.temp), False, (0, 0, 0))
            t = 0
        else:
            t += 1
        self.SCREEN.blit(self.temp_message, self.pos)

    def ignite(self):
        self.burning = True
        self.temp = self.ignition_tresh
        self.texture = (255, 0, 0)
        self.LEVEL.Burning.append(self)

    def extinguish(self):
        self.burning = False
        self.texture = (0, 255, 0)
        self.influence_rad = 0
        self.LEVEL.Burning.remove(self)

    def destroy(self):
        self.burning = False
        self.texture = (255, 255, 0)
        self.LEVEL.Burning.remove(self)
        self.STRUCTURE.Furniture.remove(self)
        self.ROOM.Furniture.remove(self)

    def burn(self):
        if self.health <= 0:
            self.destroy()
            return
        # Contain Wetness
        if self.wetness > 100:
            self.wetness = 100
        elif self.wetness < 0:
            self.wetness = 0
        # Contain Temp
        if self.temp < 30:
            self.temp = 30
        elif self.temp >= 700:
            self.temp = 600
        if self.burning:
            if self.wetness >= 100:
                self.extinguish()
                return
            elif self.temp < 700:
                self.temp += 1/self.grid_area*((100-self.wetness)/100)
            self.health -= 1/self.grid_area
        else:
            if self.isHeatingUp():
                # if self.isHeatingUp()[1]:
                self.temp += 0.1
                # if not self.isHeatingUp()[1]:
                    # self.temp += 0.005
            else:
                if self.temp > self.ROOM.temp:
                    self.temp -= 0.1
            if self.temp-2 <= self.ignition_tresh <= self.temp+2:
                self.ignite()
        self.wetness -= self.temp/100
        self.update_influence()
        self.update_rect()

    def isHeatingUp(self):
        return self.Rect.collidelist([other.influence_Rect for other in self.LEVEL.Burning]) != -1

    def cool_down(self, effect):
        self.temp -= effect/self.grid_area*2
        self.wetness += effect/self.grid_area*2

    def update_rect(self):
        self.influence_Rect = pygame.Rect(0, 0, self.length + self.influence_rad, self.width + self.influence_rad)
        self.influence_Rect.center = self.pos
        if self.temp <= self.ignition_tresh:
            self.texture = (0, 0, 255)
        elif self.ignition_tresh < self.temp <= 255:
            self.texture = (self.temp, 0, 0)
        else:
            self.texture = (255, 0, 0)

    def update_influence(self):
        if self.burning:
            self.influence = self.temp//10
            self.influence_rad = self.influence * 2
