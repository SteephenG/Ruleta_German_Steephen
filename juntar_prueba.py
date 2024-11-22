import pygame
import math
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 1700, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ruleta de Casino")

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
YELLOW = (255, 255, 0)
DARK_YELLOW = (139, 128, 0)
BROWN_LIGHT = (160, 82, 45)  # Marrón claro
BROWN_DARK = (101, 67, 33)   # Marrón oscuro
GRAY = (169, 169, 169)       # Gris
DARK_GRAY = (51, 51, 51)
GRIS_OSCURO = (34, 34, 34)

# Configuración del centro y el radio
center = (width // 2, height // 3)  # Coloca la ruleta en la parte superior
outer_radius = 350
center_radius = 50  # Radio del círculo central decorativo
middle_radius = 90  # Radio del círculo vacío adicional

# Números de la ruleta y sus colores
numbers = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24,
    16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]
colors = [GREEN] + [
    BLACK if i % 2 == 0 else RED for i in range(1, len(numbers))
]

# Variables de rotación
current_angle = 0
target_angle = 0
speed = 0
spinning = False

# Fuente para texto
font = pygame.font.SysFont(None, 35)

# Función para dibujar la ruleta con sombra y efectos
def draw_roulette():
    global current_angle

    # Dibujar círculo marrón claro en el centro
    pygame.draw.circle(screen, BROWN_LIGHT, center, 225)

    # Sombra exterior (base de madera)
    pygame.draw.circle(screen, BROWN_LIGHT, center, outer_radius + 30)  # Base marrón claro
    pygame.draw.circle(screen, BROWN_DARK, center, outer_radius + 15)   # Sombra interior de base

    # Fondo principal de la ruleta
    pygame.draw.circle(screen, GOLD, center, outer_radius)  # Borde dorado
    pygame.draw.circle(screen, BLACK, center, outer_radius - 10)  # Fondo negro

    # Dibujar los segmentos triangulares
    angle_step = 360 / len(numbers)  # Dividir en 37 partes iguales

    for i, number in enumerate(numbers):
        # Calcular ángulos y posiciones
        start_angle = math.radians(current_angle + i * angle_step)
        end_angle = math.radians(current_angle + (i + 1) * angle_step)

        # Calcular puntos para el triángulo del segmento
        x1 = center[0] + outer_radius * math.cos(start_angle)
        y1 = center[1] + outer_radius * math.sin(start_angle)
        x2 = center[0] + outer_radius * math.cos(end_angle)
        y2 = center[1] + outer_radius * math.sin(end_angle)

        # Dibujar contorno blanco del segmento
        pygame.draw.polygon(screen, WHITE, [center, (x1, y1), (x2, y2)], width=5)

        # Dibujar segmento triangular de color
        color = colors[i]
        pygame.draw.polygon(screen, color, [center, (x1, y1), (x2, y2)])

        # Dibujar los números
        mid_angle = math.radians(current_angle + (i + 0.5) * angle_step)
        text_x = center[0] + (outer_radius - 50) * math.cos(mid_angle)
        text_y = center[1] + (outer_radius - 50) * math.sin(mid_angle)
        text = font.render(str(number), True, WHITE)
        screen.blit(text, text.get_rect(center=(text_x, text_y)))

    # Bolita amarilla y gris
    pygame.draw.circle(screen, GRAY, center, 120)
    pygame.draw.circle(screen, DARK_YELLOW, center, 15)
    pygame.draw.circle(screen, YELLOW, center, 10)

# Función para dibujar la mesa de apuestas
def draw_betting_table():
    cell_width = 65
    cell_height = 80
    offset_x = 850
    offset_y = 500

    numbers = [
        [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
        [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
    ]

    # Colores de los números (rojos y negros)
    colors = {0: GREEN, **{num: RED if num % 2 == 1 else BLACK for num in range(1, 37)}}

    # Dibujar el número 0 en la mesa
    pygame.draw.rect(screen, GREEN, (offset_x, offset_y - 80, cell_width, cell_height))
    pygame.draw.rect(screen, WHITE, (offset_x, offset_y - 80, cell_width, cell_height), 2)
    text_surface = font.render("0", True, WHITE)
    screen.blit(text_surface, text_surface.get_rect(center=(offset_x + cell_width // 2, offset_y - 80 + cell_height // 2)))

    # Dibujar números de la ruleta
    for i, row in enumerate(numbers):
        for j, num in enumerate(row):
            x = offset_x + j * cell_width
            y = offset_y + i * cell_height
            color = colors.get(num, WHITE)
            pygame.draw.rect(screen, color, (x, y, cell_width, cell_height))
            pygame.draw.rect(screen, WHITE, (x, y, cell_width, cell_height), 2)
            text_surface = font.render(str(num), True, WHITE)
            screen.blit(text_surface, text_surface.get_rect(center=(x + cell_width // 2, y + cell_height // 2)))

    # Añadir las casillas de columna
    column_titles = ["1st Column", "2nd Column", "3rd Column"]
    for i, title in enumerate(column_titles):
        pygame.draw.rect(screen, WHITE, (offset_x + 780, offset_y + i * 100, 100, 40), 2)
        text_surface = font.render(title, True, WHITE)
        screen.blit(text_surface, text_surface.get_rect(center=(offset_x + 830, offset_y + i * 100 + 20)))

    # Añadir las secciones de 12, par/impar, y rojo/negro
    sections = ["1st 12", "2nd 12", "3rd 12", "Odd", "Even", "Red", "Black"]
    for i, section in enumerate(sections):
        x = offset_x + i * 120
        y = offset_y + 350
        pygame.draw.rect(screen, WHITE, (x, y, 100, 40), 2)
        text_surface = font.render(section, True, WHITE)
        screen.blit(text_surface, text_surface.get_rect(center=(x + 50, y + 20)))

# Función principal para la ruleta
def roulette():
    global current_angle, target_angle, speed, spinning

    running = True
    while running:
        screen.fill(BLACK)
        draw_roulette()
        draw_betting_table()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not spinning:
                    spinning = True
                    speed = random.randint(15, 25)
                    target_angle = random.randint(3600, 7200)

        if spinning:
            current_angle += speed
            if current_angle >= target_angle:
                spinning = False
            else:
                speed *= 0.99  # Reduce la velocidad suavemente

        pygame.display.update()

# Ejecutar el juego
roulette()
pygame.quit()
