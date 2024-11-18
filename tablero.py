import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils
# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREENF = (53, 131, 61, 1)

pygame.init()
clock = pygame.time.Clock()

# Definir la ventana
screen = pygame.display.set_mode((1100, 800))
pygame.display.set_caption('Ruleta de Casino')

# Bucle de la aplicación
def main():
    is_looping = True
    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()

        clock.tick(60) # Limitar a 60 FPS

    # Fuera del bucle, cerrar la aplicación
    pygame.quit()
    sys.exit()

# Gestionar eventos
def app_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Botón cerrar ventana
            return False
    return True

# Realizar cálculos
def app_run():
    pass

# Dibujar
def app_draw():
    # Pintar el fondo de verde
    screen.fill(GREENF)

    # Casillas del tablero (marco exterior)
    pygame.draw.rect(screen, WHITE, (300, 550, 600, 150), 4)

    # Dibujar cuadrados alternados con borde blanco
    square_size = 50  # Tamaño de cada cuadrado
    num_rows = 3  # Número de filas
    num_cols = 12  # Número de columnas

    # Números del 1 al 36 (en orden clásico de ruleta)
    numbers = [
        32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13,
        36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20,
        14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
        0  # El número 0 es verde
    ]
    
    # Colores de los números (rojo o negro, según corresponda)
    colors = []
    for num in numbers:
        if num == 0:
            colors.append(GREEN)  # El 0 es verde
        elif num % 2 == 0:
            colors.append(BLACK)  # Números pares en negro
        else:
            colors.append(RED)  # Números impares en rojo

    # Variable para llevar el índice de los números
    num_index = 0

    # Dibujar los cuadrados con números
    # Esquina del tablero
    pygame.draw.polygon(screen, WHITE, [(150, 625), (250, 550), (300, 550), (300, 700),(250, 700)],4)    
    for row in range(num_rows):
        for col in range(num_cols):
            # Calcular posición del cuadrado
            x = 300 + col * square_size
            y = 550 + row * square_size

            # Seleccionar el color del número
            color = colors[num_index]

            # Dibujar el borde blanco del cuadrado
            pygame.draw.rect(screen, WHITE, (x, y, square_size, square_size), )
            # Dibujar el interior del cuadrado
            pygame.draw.rect(screen, color, (x + 4, y + 4, square_size - 8, square_size - 8))  # Deja un margen de 4 px para el borde

            # Dibujar el número dentro del cuadrado
            number_text = str(numbers[num_index])
            num_index += 1

            # Crear fuente para el número
            font = pygame.font.Font(None, 30)
            number_surface = font.render(number_text, True, WHITE)  # Número en blanco

            # Calcular la posición para centrar el número en el cuadrado
            num_x = x + (square_size - number_surface.get_width()) // 2
            num_y = y + (square_size - number_surface.get_height()) // 2

            # Dibujar el número
            screen.blit(number_surface, (num_x, num_y))

    # Actualizar el dibujo en la ventana
    pygame.display.update()  

if __name__ == "__main__":
    main()
