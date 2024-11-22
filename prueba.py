import pygame
import math
import random

# Funciones desde los archivos de la ruleta y la mesa de apuestas
from rulleta import draw_roulette, draw_arrow
from mesadeapuestas import draw_betting_table, draw_special_rectangle, draw_external_bets

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 1700, 900  # Un tamaño más grande para albergar ambos
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ruleta de Casino y Mesa de Apuestas")

# Colores
BLACK = (0, 0, 0)

# Ajustes de la ruleta
RULETTE_WIDTH = 800
RULETTE_HEIGHT = 800

# Función para dibujar la interfaz combinada
def draw_combined_interface():
    # Dibuja la ruleta en la parte izquierda de la pantalla (ajustamos las coordenadas para que se dibuje en la izquierda)
    draw_roulette()

    # Dibuja la mesa de apuestas a la derecha de la pantalla
    # La mesa de apuestas debe ser dibujada dentro de las coordenadas correctas para evitar que se solape
    draw_betting_table()
    draw_special_rectangle()
    draw_external_bets()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fondo
    screen.fill(BLACK)
    
    # Dibuja ambos elementos (ruleta y mesa de apuestas) en la misma pantalla
    draw_combined_interface()

    # Actualiza la pantalla
    pygame.display.flip()

    pygame.time.Clock().tick(60)  # FPS (Frames por segundo)

pygame.quit()
