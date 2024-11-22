import pygame
import math
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 800, 800
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
BUTTON_COLOR = (0, 102, 204)
BUTTON_HOVER_COLOR = (0, 153, 255)

# Configuración del centro y el radio
center = (width // 2, height // 2)
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
]  # Alternancia entre negro y rojo, comenzando por negro.

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

    # Dibujar el contorno negro del círculo exterior
    pygame.draw.circle(screen, BLACK, center, outer_radius + 30, 4)  # Contorno negro

    # Dibujar el contorno negro del círculo interior
    pygame.draw.circle(screen, BLACK, center, outer_radius + 15, 4)  # Contorno negro

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

    # circulo marron
    pygame.draw.circle(screen, BROWN_LIGHT, center, 200)  
    pygame.draw.circle(screen, BROWN_DARK, center, 180)  

    # borde negro principal
    pygame.draw.circle(screen, BLACK, center, 200, 4)  # Línea exterior marrón más gruesa

    # circulo gris
    pygame.draw.circle(screen, GRAY, center, 137)

    # sombras grises
    pygame.draw.circle(screen, (169, 169, 169, 100), center, 137 + 5)  # Sombra ligera en gris
    pygame.draw.circle(screen, (51, 51, 51, 100), center, 130 + 5)  # Sombra ligera en gris
    pygame.draw.circle(screen, (34, 34, 34, 100), center, 117 + 5)


    # bolita amarilla y gris
    pygame.draw.circle(screen, GRAY, center, 120)
    pygame.draw.circle(screen, DARK_YELLOW, center, 15)
    pygame.draw.circle(screen, YELLOW, center, 10)



    # lineas pa hacer bonito
    pygame.draw.circle(screen, WHITE, center, 225, 3)  # Círculo negro sin relleno
    pygame.draw.circle(screen, BLACK, center, 215, 3)
    pygame.draw.circle(screen, WHITE, center, 255, 3)
    pygame.draw.circle(screen, BLACK, center, 20, 1)
    pygame.draw.circle(screen, BLACK, center, 137, 3)
    pygame.draw.circle(screen, DARK_GRAY, center, 115, 30)
    pygame.draw.circle(screen, BLACK, center, 145, 3)
    pygame.draw.circle(screen, BLACK, center, 86, 4)
    pygame.draw.circle(screen, BLACK, center, 150, 3)
    pygame.draw.circle(screen, BLACK, center, 115, 3)
    pygame.draw.circle(screen, BLACK, center, 120, 3)
    pygame.draw.circle(screen, BLACK, center, 18, 3)
    pygame.draw.circle(screen, BLACK, center, 350, 4)
    pygame.draw.circle(screen, BLACK, center, 352, 3)
    pygame.draw.circle(screen, BLACK, center, 181, 2)

# Dibujar flecha fija hacia abajo, tocando la ruleta
def draw_arrow():
    pygame.draw.polygon(screen, YELLOW, [
        (center[0], center[1] - outer_radius),  # Base de la flecha (en el centro)
        (center[0] - 20, center[1] - outer_radius - 40),  # Punta de la flecha (apunta hacia abajo)
        (center[0] + 20, center[1] - outer_radius - 40)   # Derecha
    ])
    pygame.draw.polygon(screen, BLACK, [
        (center[0], center[1] - outer_radius),  # Base de la flecha (en el centro)
        (center[0] - 20, center[1] - outer_radius - 40),  # Punta de la flecha (apunta hacia abajo)
        (center[0] + 20, center[1] - outer_radius - 40)   # Derecha
    ], width=2)

# Dibujar botón
def draw_button(x, y, w, h, text, hover):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, text_surface.get_rect(center=(x + w // 2, y + h // 2)))

# Función principal para el bucle de la ruleta
def roulette():
    global current_angle, target_angle, speed, spinning

    running = True
    while running:
        screen.fill(BLACK)
        draw_roulette()
        draw_arrow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not spinning:  # Comienza la ruleta si no está girando
                    spinning = True
                    speed = random.randint(15, 25)
                    target_angle = random.randint(3600, 7200)  # Un rango mayor de vueltas

        if spinning:
            current_angle += speed
            if current_angle >= target_angle:
                spinning = False
                current_angle = target_angle
            else:
                speed *= 0.99  # Desaceleración más gradual

        pygame.display.update()
        pygame.time.Clock().tick(60)  # FPS (Frames por segundo)

    pygame.quit()

# Ejecutar la ruleta
roulette()
