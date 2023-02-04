import os
import sys

import pygame
import requests

LON, LAT = "70", "70"
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
size = (600, 450)
screen = pygame.display.set_mode(size)
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
            if event.key == pygame.K_UP:
                temp = float(LAT) + float(f'0.{size[-1] // 2}')
                if temp < 80.0:
                    LAT = str(temp)
                    drow_map()
            if event.key == pygame.K_DOWN:
                temp = float(LAT) - float(f'0.{size[-1] * (24 - Z)}')
                if temp > -80.0:
                    LAT = str(temp)
                    drow_map()
            if event.key == pygame.K_LEFT:
                temp = float(LON) - float(f'0.{size[0] * (24 - Z)}')
                if temp > -180.0:
                    LON = str(temp)
                    drow_map()
            if event.key == pygame.K_RIGHT:
                temp = float(LON) + float(f'0.{size[0] * (24 - Z)}')
                if temp < 180.0:
                    LON = str(temp)
                    drow_map()
pygame.quit()

os.remove(map_file)
