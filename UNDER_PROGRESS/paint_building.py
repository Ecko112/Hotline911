import pygame


def paint_building(screen, building):
    for room in building.Rooms:
        paint_room(screen, room)


def paint_room(screen, room):
    polyroom = [room.p1, room.p2, room.p3, room.p4, room.p5, room.p6]
    floor_text = room.floor
    wall_text = room.wall
    epaisseur = room.wall

    pygame.draw.polygon(screen, floor_text, polyroom)
    pygame.draw.polygon(screen, wall_text, polyroom, epaisseur)
