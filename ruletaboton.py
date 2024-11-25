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
]  # Alternancia entre negro y rojo, comenzando por verde para el 0.

# Variables de rotación
current_angle = 270  # La ruleta comienza apuntando a 270 grados
target_angle = 0
speed = 0
spinning = False
final_number = None  # Variable para almacenar el número final

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

    # Circulo central
    pygame.draw.circle(screen, BROWN_LIGHT, center, 200)
    pygame.draw.circle(screen, BROWN_DARK, center, 180)

    # Borde negro
    pygame.draw.circle(screen, BLACK, center, 200, 4)  # Línea exterior

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

# Dibujar el número que salió
def draw_number_wheel():
    if final_number is not None:
        text = font.render(f"Número: {final_number}", True, WHITE)
        screen.blit(text, (width // 2 - text.get_width() // 2, height - 100))

# Función para dibujar un botón
def draw_button(x, y, w, h, text, hover=False):
    color = BUTTON_COLOR if not hover else BUTTON_HOVER_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h))
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x + (w - text_surface.get_width()) // 2, y + (h - text_surface.get_height()) // 2))

# Función para obtener el número final en base al ángulo
def get_number_from_angle(angle):
    # Número de grados por cada segmento (segmentos = 37)
    segment_angle = 360 / len(numbers)
    
    # Calculamos el índice basándonos en la posición del ángulo
    angle_normalized = (angle + 360) % 360  # Aseguramos que el ángulo esté entre 0 y 360
    index = int((angle_normalized) // segment_angle)  # Dividimos por el tamaño del segmento para obtener el índice
    return numbers[index]

# Control del juego
def main():
    global spinning, target_angle, current_angle, speed, final_number

    running = True
    while running:
        screen.fill(BLACK)
        draw_roulette()
        draw_arrow()

        # Gestionar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Botón para girar la ruleta
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_rect = pygame.Rect(width // 2 - 100, height - 150, 200, 50)
        draw_button(width // 2 - 100, height - 150, 200, 50, "Girar Ruleta", button_rect.collidepoint(mouse_x, mouse_y))

        if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(mouse_x, mouse_y) and not spinning:
            spinning = True
            target_angle = random.randint(500, 1000)  # Ángulo de destino aleatorio
            speed = random.randint(10, 20)  # Velocidad aleatoria

        # Movimiento de la ruleta
        if spinning:
            current_angle += speed
            speed *= 0.99  # Desaceleración suave
            if speed < 0.1:
                spinning = False
                final_number = get_number_from_angle(current_angle)

        # Dibujar el número que salió
        draw_number_wheel()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Ejecutar el juego
main()
pygame.quit()
