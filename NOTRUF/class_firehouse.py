import pygame
clock = pygame.time.Clock()

X = 0
Y = 1


class Firehouse:
    ################
    # KEY BINDINGS #
    ################
    # [DEV]
    # FORCE START LEVEL
    FORCE_START_LEVEL = pygame.K_BACKSPACE

    def __init__(self, MAIN):
        self.MAIN = MAIN
        self.SCREEN = self.MAIN.SCREEN
        self.SCREEN_RESOLUTION = self.MAIN.SCREEN_RESOLUTION
        ############
        # TEXTURES #
        ############
        self.HERBE_TEXTURE = self.MAIN.GREEN
        self.BETON_TEXTURE = self.MAIN.LIGHT_GREY
        self.BITUME_TEXTURE = self.MAIN.DARK_GREY

    def loop_firehouse(self):

        self.process_input()
        self.paint_firehouse()
        # Lock 50 FPS
        clock.tick(50)

    def paint_firehouse(self):
        # Background
        self.SCREEN.fill(self.HERBE_TEXTURE)
        # Update screen
        pygame.display.flip()

    def process_input(self):
        pass
