import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils

# Definir colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0) 

pygame.init()
clock = pygame.time.Clock()

# Definir la finestra
screen = pygame.display.set_mode((1000,800))
pygame.display.set_caption('Window Title')

# Bucle de l'aplicació
def main():
    global im_ruleta
    is_looping = True

    path_ruleta = os.path.join(os.path.dirname(__file__), "Imagenes/Ruleta.png")
    im_ruleta = pygame.image.load(path_ruleta). convert_alpha()
    im_ruleta = utils.scale_image(pygame, im_ruleta, target_width=600)
    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()

        clock.tick(60) # Limitar a 60 FPS

    # Fora del bucle, tancar l'aplicació
    pygame.quit()
    sys.exit()

# Gestionar events
def app_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Botó tancar finestra
            return False
    return True

# Fer càlculs
def app_run():
    pass

# Dibuixar
def app_draw():
    global im_ruleta
    # Pintar el fons de blanc
    screen.fill(WHITE)

    screen.blit(im_ruleta, (325, 160))
    # Escriure un text de prova
    font = pygame.font.SysFont("Arial", 55)
    text = font.render('Hello World!', True, BLACK)
    screen.blit(text, (50, 50))



    # Actualitzar el dibuix a la finestra
    pygame.display.update()

if __name__ == "__main__":
    main()