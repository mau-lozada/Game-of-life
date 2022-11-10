import sys, pygame
import numpy as np
import matplotlib.pyplot as plt
import time

pygame.init()

size = width, height = 600, 600

#Número de celdas
nxC = 30
nyC = 30

#Dimensiones de la celda
dimCW = (width - 1) / nxC
dimCH = (height - 1) / nyC

bg = 25, 25, 25

screen = pygame.display.set_mode(size)

#Pintamos el fondo con el color elegido
screen.fill(bg)

#Estado de las celdas. Vivas = 1; Muertas = 0
gameState = np.zeros((nxC, nyC))

#gameState[21, 21] = 1
#gameState[22, 22] = 1
#gameState[22, 23] = 1
#gameState[21, 23] = 1
#gameState[20, 23] = 1


print(gameState)

#Control de la ejecución del juego
pauseExect = False

while 1:

    #Guardamos cada iteración del juego
    new_gameState = np.copy(gameState)

    screen.fill(bg)

    #Registramos eventos de teclado y ratón
    ev = pygame.event. get()

    for event in ev:
        #Detectamos si se presiona el espacio del teclado
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        #Detectamos si se presiona el ratón.
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            new_gameState[celX, celY] = not mouseClick[2]

    for y in range(0, nyC):
        for x in range(0, nxC):

            if not pauseExect:
                #Calculamos el número de vecinos cercanos. (el % es para hacerlo toroidal)
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                          gameState[(x) % nxC, (y - 1) % nyC] + \
                          gameState[(x+1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1 ) % nxC, (y) % nyC] + \
                          gameState[(x + 1) % nxC, (y) % nyC] + \
                          gameState[(x-1) % nxC, (y+1) % nyC] + \
                          gameState[(x) % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC]


                #Una célula muerta con exactamente 3 células vecinas vivas "nace"
                if gameState[x, y] == 0 and n_neigh == 3:
                    new_gameState[x, y] = 1

                #Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere

                elif gameState[x, y] == 1 and (n_neigh < 2 or  n_neigh > 3):
                    new_gameState[x, y] = 0

            #Creamos el polígono de cada celda a dibujar
            poly = [((x) * dimCW, (y) * dimCH),
                        ((x+1) * dimCW,     (y) * dimCH),
                        ((x+1) * dimCW,     (y+1) * dimCH),
                        ((x) * dimCW, (y+1) * dimCH)]

            #Y creamos la celda para cada par de x e y.
            if new_gameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    #Actualizamos el estado del juego

    gameState = np.copy(new_gameState)

    #Delay
    time.sleep(0.1)

    #Actualizamos la pantalla
    pygame.display.flip()
