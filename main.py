import os
import sys

import pygame
import requests

LON, LAT = "39.568664", "52.628096"
Z = 12
api_server = "http://static-maps.yandex.ru/1.x/"


def drow_map():
    params = {
        "ll": ",".join([LON, LAT]),
        "z": Z,
        "l": "map"
    }
    response = requests.get(api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((600, 450))
map_file = "map.png"
drow_map()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if Z < 23:
                    Z += 1
                    drow_map()
            if event.key == pygame.K_PAGEDOWN:
                if Z > 0:
                    Z -= 1
                    drow_map()

    # screen.fill((0, 0, 0))
    # pygame.display.flip()
pygame.quit()

os.remove(map_file)
