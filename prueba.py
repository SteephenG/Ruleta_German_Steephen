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

# Función para dibujar la ruleta
def draw_roulette():
    global current_angle

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
        pygame.draw.polygon(screen, WHITE, [center, (x1, y1), (x2, y2)], width=2)

        # Dibujar segmento triangular de color
        color = colors[i]
        pygame.draw.polygon(screen, color, [center, (x1, y1), (x2, y2)])

        # Dibujar los números
        mid_angle = math.radians(current_angle + (i + 0.5) * angle_step)
        text_x = center[0] + (outer_radius - 50) * math.cos(mid_angle)
        text_y = center[1] + (outer_radius - 50) * math.sin(mid_angle)
        text = font.render(str(number), True, WHITE)
        screen.blit(text, text.get_rect(center=(text_x, text_y)))

    # Dibujar círculo blanco adicional
    pygame.draw.circle(screen, WHITE, center, middle_radius)

    # Dibujar borde negro para el círculo adicional
    pygame.draw.circle(screen, BLACK, center, middle_radius, 2)

    # Dibujar círculo central blanco
    pygame.draw.circle(screen, WHITE, center, center_radius)

    # Dibujar borde negro para el círculo central
    pygame.draw.circle(screen, BLACK, center, center_radius, 2)

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

# Lógica para hacer girar la ruleta
def spin_roulette():
    global target_angle, speed, spinning

    # Elegir un giro aleatorio
    steps = random.randint(3, 5) * 360  # Giros completos
    offset = random.randint(0, 360)     # Desplazamiento final
    target_angle = current_angle + steps + offset
    speed = 20  # Velocidad inicial alta
    spinning = True

# Bucle principal
running = True
button_rect = pygame.Rect(300, 700, 200, 50)  # Posición y tamaño del botón

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and not spinning:
                spin_roulette()

    # Fondo de pantalla
    screen.fill(WHITE)

    # Dibujar ruleta
    draw_roulette()

    # Dibujar flecha fija
    draw_arrow()

    # Dibujar botón
    mouse_pos = pygame.mouse.get_pos()
    draw_button(button_rect.x, button_rect.y, button_rect.width, button_rect.height, "GIRAR", button_rect.collidepoint(mouse_pos))

    # Girar la ruleta con desaceleración
    if spinning:
        if current_angle < target_angle:
            current_angle += speed
            speed *= 0.98  # Reducir velocidad gradualmente
            if speed < 0.35:  # Límite mínimo de velocidad
                speed = 0.35
        else:
            spinning = False  # Detener el giro
            current_angle %= 360  # Ajustar el ángulo actual

    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
