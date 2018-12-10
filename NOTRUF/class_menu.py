import pygame
# import math
pygame.font.init()
clock = pygame.time.Clock()

X = 0
Y = 1


class Menu:
    ################
    # KEY BINDINGS #
    ################
    # [DEV]
    # FORCE START LEVEL
    FORCE_START_LEVEL = pygame.K_BACKSPACE
    # Polices

    def __init__(self, MAIN):
        # INIT
        self.MAIN = MAIN
        self.SCREEN = self.MAIN.SCREEN
        self.SCREEN_RESOLUTION = self.MAIN.SCREEN_RESOLUTION
        self.Buttons = []
        # Set Logo
        self.logo_size = (int(self.SCREEN_RESOLUTION[X]//1.5/2), int(self.SCREEN_RESOLUTION[X]//9.04/2))
        self.logo_pos = [2*self.SCREEN_RESOLUTION[X]/100, 2*self.SCREEN_RESOLUTION[X]/100]
        self.logo_png = pygame.image.load('/home/louis/Documents/Universite/INFO2056/notruf112/UNDER_PROGRESS/IMAGES/logo908x151.png').convert_alpha(self.SCREEN)
        self.logo_png = pygame.transform.scale(self.logo_png, self.logo_size)

        # Set Start Level
        self.start_level_font_size = int(self.SCREEN_RESOLUTION[X] // 39.02)
        self.start_level_font = pygame.font.SysFont('monospace', self.start_level_font_size)
        self.start_level = Button(" Start New Level ", self.start_level_font, (255, 255, 255), (255, 0, 0), self)
        self.start_level.pos = [2*self.SCREEN_RESOLUTION[X]/100, 30*self.SCREEN_RESOLUTION[Y]//100]

        # Set Exit Game
        self.exit_game_font_size = int(self.SCREEN_RESOLUTION[X]//39.02)
        self.exit_game_font = pygame.font.SysFont('monospace', self.exit_game_font_size)
        self.exit_game = Button(" Exit Game ", self.exit_game_font, (255, 255, 255), (255, 0, 0), self)
        self.exit_game.pos = [2*self.SCREEN_RESOLUTION[X]/100, 37*self.SCREEN_RESOLUTION[Y]//100]

    def loop_menu(self):
        self.process_input()
        self.paint_menu()
        # LOCK 10 FPS
        clock.tick(10)

    def paint_menu(self):
        # Background
        self.SCREEN.fill((100, 100, 100))
        # Logo
        self.SCREEN.blit(self.logo_png, self.logo_pos)
        # Buttons
        # Start Level
        self.start_level.paint_button()
        # Exit
        self.exit_game.paint_button()
        # Update screen
        pygame.display.flip()

    def process_input(self):
        # KEYBOARD INPUT
        key_input = pygame.key.get_pressed()
        # [DEV] FORCE START LEVEL
        if key_input[self.FORCE_START_LEVEL]:
            self.MAIN.create_level()
        # MOUSE INPUT
        mouse_pos = pygame.mouse.get_pos()
        mouse_input = pygame.mouse.get_pressed()
        if mouse_input[0]:
            for button in self.Buttons:
                if button.title.get_rect(topleft=button.pos).collidepoint(mouse_pos):
                    if button is self.exit_game:
                        self.MAIN.exit_game()
                    elif button is self.start_level:
                        self.MAIN.create_level()


class Button:

    def __init__(self, text, font, font_color, back_color, MENU):
        # INIT
        self.MENU = MENU
        self.MAIN = self.MENU.MAIN
        self.SCREEN = self.MENU.SCREEN
        self.pos = [0, 0]
        # Set Text
        self.text = text
        self.font = font
        self.font_color = font_color
        self.back_color = back_color
        self.size = self.font.size(self.text)
        # Create Surface
        self.title = self.font.render(text, True, self.font_color, self.back_color)
        self.MENU.Buttons.append(self)

    def paint_button(self):
        self.SCREEN.blit(self.title, self.pos)
