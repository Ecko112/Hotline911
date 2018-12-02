import pygame
import math
import random
import time

# ---- CSTES ---------------------------------------------

X = 0
Y = 1

VERT_HERBE = (0, 153, 0)
ROUGE = (255, 0, 0)
GRIS = (169, 169, 169)
MUR = (128, 128, 128)
ROUTE = (32, 32, 32)
ECRAN_TAILLE = (1366, 768)

UPPER_LEFT = (ECRAN_TAILLE[X]//20, ECRAN_TAILLE[X]//20)
UPPER_RGHT = (ECRAN_TAILLE[X]-ECRAN_TAILLE[X]//20, ECRAN_TAILLE[X]//20)
LOWER_LEFT = (ECRAN_TAILLE[X]//20, 3*ECRAN_TAILLE[Y]//4)
LOWER_RGHT = (ECRAN_TAILLE[X]-ECRAN_TAILLE[X]//20, 3*ECRAN_TAILLE[Y]//4)

ZONE = (UPPER_RGHT[X]-UPPER_LEFT[X], LOWER_RGHT[Y]-UPPER_RGHT[Y])
ZONEL = ZONE[X]
ZONEl = ZONE[Y]

ROUTEH = (0, 1*ECRAN_TAILLE[Y]//10)


MUR_EPAISSEUR = 10

PLAYER_SIZE = ECRAN_TAILLE[Y]//40
STEP = PLAYER_SIZE // 3
COULOIR = PLAYER_SIZE*3

ROOMS = 6

# ---- VARIABLES --------------------------------------------


# ---- INPUT -------------------------------------------
# MOVEMENT


UP = pygame.K_z
DOWN = pygame.K_s
LEFT = pygame.K_q
RGHT = pygame.K_d

up = left = -1
down = rght = 1


def player_mov(dirx, x, diry, y):
    if x:
        player['pos'][X] += STEP*dirx
    if y:
        player['pos'][Y] += STEP*diry


# ---- FONCTIONS ---------------------------------------------


def premier_dessin():
    ECRAN.fill(VERT_HERBE)


def paint():
    ECRAN.fill(VERT_HERBE)
    pygame.draw.rect(ECRAN, ROUTE, (ROUTEH, (ECRAN_TAILLE[X], ROUTEH[Y])))
    pygame.draw.circle(ECRAN, ROUGE, player['pos'], PLAYER_SIZE)


def paint_roum(room):
    if room == 'room_1':
        pygame.draw.rect(ECRAN, room_1['sol'], ((room_1['pos']), (room_1['zone'])))
    if room == 'room_2':
        pygame.draw.rect(ECRAN, room_2['sol'], ((room_2['pos']), (room_2['zone'])))
    if room == 'room_3':
        pygame.draw.rect(ECRAN, room_3['sol'], ((room_3['pos']), (room_3['zone'])))



def paint_test():
    pygame.draw.rect(ECRAN, GRIS, (UPPER_LEFT, ZONE))
    pygame.draw.rect(ECRAN, MUR, (UPPER_LEFT, (ZONE[X], 10)))
    pygame.draw.circle(ECRAN, GRIS, LOWER_LEFT, 2)
    pygame.draw.circle(ECRAN, GRIS, LOWER_RGHT, 2)
    pygame.draw.circle(ECRAN, GRIS, UPPER_LEFT, 2)
    pygame.draw.circle(ECRAN, GRIS, UPPER_RGHT, 2)


def traites_entrees():
    global gameover
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            gameover = True

        input = pygame.key.get_pressed()

        if input[UP]:
            player_mov(0, False, up, True)
        elif input[DOWN]:
            player_mov(0, False, down, True)
        if input[RGHT]:
            player_mov(rght, True, 0, False)
        elif input[LEFT]:
            player_mov(left, True, 0, False)


# #### PYGAME.INIT()  ########################################
# #### INITIALISATION ########################################


pygame.init()
pygame.key.set_repeat(1, 50)

random.seed()

ECRAN = pygame.display.set_mode(ECRAN_TAILLE)

temps = pygame.time.Clock()

gameover = False

print('ca marche')

player = add_player(700, 500, ROUGE)
premier_dessin()

# room_1 = add_room(bat, 'room_1', (5*PLAYER_SIZE)-MUR_EPAISSEUR, 3*ZONEl//5, UPPER_LEFT[X], UPPER_LEFT[Y], GRIS)
# room_2 = add_room(bat, 'room_2', 4*ZONEL//10, 3*ZONEl//5, UPPER_LEFT[X]+4*ZONEL//10, UPPER_LEFT[Y], ROUGE)
# room_3 = add_room(bat, 'room_3', 2*ZONEL//10, 3*ZONEl//5, UPPER_LEFT[X]+8*ZONEL//10, UPPER_LEFT[Y], ROUTE)


# #### MAIN LOOP #############################
while not gameover:
    traites_entrees()

    paint()

    pygame.display.flip()
    temps.tick(50)


pygame.display.quit()
pygame.quit()
