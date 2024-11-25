import pygame
import math
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla (ancho y alto ajustados para mostrar ambos elementos)
width, height = 1920, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ruleta de Casino y Mesa de Apuestas")

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
YELLOW = (255, 255, 0)
DARK_YELLOW = (139, 128, 0)
BROWN_LIGHT = (160, 82, 45)
BROWN_DARK = (101, 67, 33)
GRAY = (169, 169, 169)
DARK_GRAY = (51, 51, 51)
LIGHT_GRAY = (169, 169, 169)
DARK_RED = (139, 0, 0)
DARK_BLACK = (50, 50, 50)
GREENF = (53, 131, 61)
GREENB = (77, 115, 61)

# Fuente para texto
font = pygame.font.SysFont("Times New Roman", 25)

# Configuración de la ruleta
center = (400, height // 2)
outer_radius = 350
center_radius = 50

numbers = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24,
    16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]
colors = [GREEN] + [
    BLACK if i % 2 == 0 else RED for i in range(1, len(numbers))
]

current_angle = 0
target_angle = 0
speed = 0
spinning = False

# Datos de la mesa de apuestas
bet_numbers = [
    [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
    [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
    [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
]
bet_colors = {
    0: GREEN,
    **{num: RED if num in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] else BLACK for num in range(1, 37)}
}

# Función para dibujar la ruleta
def draw_roulette():
    global current_angle
    pygame.draw.circle(screen, BROWN_LIGHT, center, outer_radius + 30)
    pygame.draw.circle(screen, BROWN_DARK, center, outer_radius + 15)
    pygame.draw.circle(screen, GOLD, center, outer_radius)
    pygame.draw.circle(screen, BLACK, center, outer_radius - 10)
    angle_step = 360 / len(numbers)

    for i, number in enumerate(numbers):
        start_angle = math.radians(current_angle + i * angle_step)
        end_angle = math.radians(current_angle + (i + 1) * angle_step)
        x1 = center[0] + outer_radius * math.cos(start_angle)
        y1 = center[1] + outer_radius * math.sin(start_angle)
        x2 = center[0] + outer_radius * math.cos(end_angle)
        y2 = center[1] + outer_radius * math.sin(end_angle)
        color = colors[i]
        pygame.draw.polygon(screen, color, [center, (x1, y1), (x2, y2)])
        mid_angle = math.radians(current_angle + (i + 0.5) * angle_step)
        text_x = center[0] + (outer_radius - 50) * math.cos(mid_angle)
        text_y = center[1] + (outer_radius - 50) * math.sin(mid_angle)
        text = font.render(str(number), True, WHITE)
        screen.blit(text, text.get_rect(center=(text_x, text_y)))

    pygame.draw.circle(screen, BROWN_LIGHT, center, 200)
    pygame.draw.circle(screen, BROWN_DARK, center, 180)
    pygame.draw.circle(screen, GRAY, center, 137)
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

# Función para dibujar la flecha
def draw_arrow():
    pygame.draw.polygon(screen, YELLOW, [
        (center[0], center[1] - outer_radius),
        (center[0] - 20, center[1] - outer_radius - 40),
        (center[0] + 20, center[1] - outer_radius - 40)
    ])
    pygame.draw.polygon(screen, BLACK, [
        (center[0], center[1] - outer_radius),
        (center[0] - 20, center[1] - outer_radius - 40),
        (center[0] + 20, center[1] - outer_radius - 40)
    ], width=2)

# Función para dibujar la mesa de apuestas
def draw_betting_table():
    cell_width = 65
    cell_height = 80
    offset_x = 950
    offset_y = 200

    # Dibujar las casillas numéricas
    for i, row in enumerate(bet_numbers):
        for j, num in enumerate(row):
            x = offset_x + j * cell_width
            y = offset_y + i * cell_height
            color = bet_colors.get(num, LIGHT_GRAY)
            pygame.draw.rect(screen, color, (x, y, cell_width, cell_height))
            pygame.draw.rect(screen, WHITE, (x, y, cell_width, cell_height), 2)
            text_surface = font.render(str(num), True, WHITE)
            screen.blit(text_surface, text_surface.get_rect(center=(x + cell_width // 2, y + cell_height // 2)))

        # Dibujar "2-1" al lado de cada fila con fondo verde
        x_2to1 = offset_x + len(row) * cell_width
        y_2to1 = offset_y + i * cell_height
        pygame.draw.rect(screen, GREENF, (x_2to1, y_2to1, cell_width, cell_height))
        pygame.draw.rect(screen, WHITE, (x_2to1, y_2to1, cell_width, cell_height), 2)
        text_surface = font.render("2-1", True, WHITE)
        screen.blit(text_surface, text_surface.get_rect(center=(x_2to1 + cell_width // 2, y_2to1 + cell_height // 2)))

            # Dibujar el "0"
    zero_x, zero_y, zero_width, zero_height = 850, 200, 100, 240
    pygame.draw.rect(screen, GREENF, (zero_x, zero_y, zero_width, zero_height))
    pygame.draw.rect(screen, WHITE, (zero_x, zero_y, zero_width, zero_height), 4)

    text_zero = font.render("0", True, WHITE)
    rotated_zero = pygame.transform.rotate(text_zero, 90)
    rotated_zero_rect = rotated_zero.get_rect(center=(zero_x + zero_width // 2, zero_y + zero_height // 2))
    screen.blit(rotated_zero, rotated_zero_rect)


    # Dibujar las casillas de docenas
    for i, label in enumerate(["1st 12", "2nd 12", "3rd 12"]):
        x = offset_x + i * 4 * cell_width
        y = offset_y + 3 * cell_height
        pygame.draw.rect(screen, DARK_GRAY, (x, y, 4 * cell_width, cell_height))
        pygame.draw.rect(screen, WHITE, (x, y, 4 * cell_width, cell_height), 2)
        text_surface = font.render(label, True, WHITE)
        screen.blit(text_surface, text_surface.get_rect(center=(x + 2 * cell_width, y + cell_height // 2)))

    # Dibujar las casillas adicionales
    extra_labels = ["1 to 18", "PAR", "ROJAS", "NEGRAS", "IMPAR", "19 to 36"]
    extra_colors = [GREENF, DARK_BLACK, RED, BLACK, DARK_BLACK, GREENF]
    extra_width = 2 * cell_width
    for i, (label, color) in enumerate(zip(extra_labels, extra_colors)):
        x = offset_x + i * extra_width
        y = offset_y + 4 * cell_height
        pygame.draw.rect(screen, color, (x, y, extra_width, cell_height))
        pygame.draw.rect(screen, WHITE, (x, y, extra_width, cell_height), 2)
        text_surface = font.render(label, True, WHITE)
        screen.blit(text_surface, text_surface.get_rect(center=(x + extra_width // 2, y + cell_height // 2)))

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not spinning:
                spinning = True
                speed = random.randint(15, 25)
                target_angle = random.randint(3600, 7200)

    screen.fill(GREENB)  # Fondo verde de la mesa
    draw_roulette()  # Dibuja la ruleta
    draw_arrow()  # Dibuja la flecha
    draw_betting_table()  # Dibuja la mesa de apuestas

    # Lógica de giro de la ruleta
    if spinning:
        current_angle += speed
        if current_angle >= target_angle:
            spinning = False
            current_angle = target_angle
        else:
            speed *= 0.99

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
