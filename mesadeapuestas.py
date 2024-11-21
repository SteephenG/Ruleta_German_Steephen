import pygame
import utils

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 1700, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mesa de Apuestas - Ruleta de Casino")

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (169, 169, 169)
DARK_RED = (139, 0, 0)
DARK_BLACK = (50, 50, 50)
GREENF = (53, 131, 61)
GREENB = (77, 115, 61)

# Fuente para el texto
font = pygame.font.SysFont("Times New Roman", 25)

# Datos de la mesa de apuestas
numbers = [
    [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],  # Primera fila
    [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],  # Segunda fila
    [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]   # Tercera fila
]

# Colores de los números (rojos y negros)
colors = {
    0: GREEN,
    **{num: RED if num in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] else BLACK for num in range(1, 37)}
}

# Función para dibujar la mesa de apuestas
def draw_betting_table():
    cell_width = 65
    cell_height = 80
    offset_x = 850
    offset_y = 500

    # Dibujar números
    for i, row in enumerate(numbers):
        for j, num in enumerate(row):
            x = offset_x + j * cell_width
            y = offset_y + i * cell_height

            # Dibujar celda y texto
            color = colors.get(num, LIGHT_GRAY)
            pygame.draw.rect(screen, color, (x, y, cell_width, cell_height))
            pygame.draw.rect(screen, WHITE, (x, y, cell_width, cell_height), 2)
            text_surface = font.render(str(num), True, WHITE)
            screen.blit(text_surface, text_surface.get_rect(center=(x + cell_width // 2, y + cell_height // 2)))

    # Dibujar el "0"
    zero_x, zero_y, zero_width, zero_height = 750, 500, 100, 240
    pygame.draw.rect(screen, GREENF, (zero_x, zero_y, zero_width, zero_height))
    pygame.draw.rect(screen, WHITE, (zero_x, zero_y, zero_width, zero_height), 4)

    text_zero = font.render("0", True, WHITE)
    rotated_zero = pygame.transform.rotate(text_zero, 90)
    rotated_zero_rect = rotated_zero.get_rect(center=(zero_x + zero_width // 2, zero_y + zero_height // 2))
    screen.blit(rotated_zero, rotated_zero_rect)

# Función para dibujar el rectángulo dividido en 3 casillas con "1 - 2" rotado
def draw_special_rectangle():
    rect_x, rect_y, rect_width, rect_height = 1630, 500, 60, 240
    num_cells = 3
    cell_height = rect_height // num_cells

    for i in range(num_cells):
        cell_y = rect_y + i * cell_height
        pygame.draw.rect(screen, WHITE, (rect_x, cell_y, rect_width, cell_height), 2)

        # Dibujar el texto "1 - 2" centrado y rotado 90 grados
        text = font.render("1 - 2", True, WHITE)
        rotated_text = pygame.transform.rotate(text, 90)
        rotated_text_rect = rotated_text.get_rect(center=(rect_x + rect_width // 2, cell_y + cell_height // 2))
        screen.blit(rotated_text, rotated_text_rect)

# Función para dibujar apuestas externas
def draw_external_bets():
    cell_width = 65
    cell_height = 50
    offset_x = 850
    offset_y = 550
    external_bets = [
        ("1st 12", offset_x, offset_y + len(numbers) * cell_height + 40, 4),
        ("1 to 18", offset_x, offset_y + len(numbers) * cell_height + 90, 2),
        ("PAR", offset_x + 2 * cell_width, offset_y + len(numbers) * cell_height + 90, 2),
        ("2nd 12", offset_x + 4 * cell_width, offset_y + len(numbers) * cell_height + 40, 4),
        ("ROJAS", offset_x + 4 * cell_width, offset_y + len(numbers) * cell_height + 90, 2),
        ("NEGRAS", offset_x + 6 * cell_width, offset_y + len(numbers) * cell_height + 90, 2),
        ("3rd 12", offset_x + 8 * cell_width, offset_y + len(numbers) * cell_height + 40, 4),
        ("IMPAR", offset_x + 8 * cell_width, offset_y + len(numbers) * cell_height + 90, 2),
        ("19 to 36", offset_x + 10 * cell_width, offset_y + len(numbers) * cell_height + 90, 2),
    ]

    for bet, x, y, *width_mult in external_bets:
        w = cell_width * (width_mult[0] if width_mult else 2)
        h = cell_height

        color = DARK_RED if bet == "ROJAS" else DARK_BLACK if bet == "NEGRAS" else LIGHT_GRAY
        pygame.draw.rect(screen, color, (x, y, w, h))
        pygame.draw.rect(screen, WHITE, (x, y, w, h), 2)

        text_surface = font.render(bet, True, BLACK)
        screen.blit(text_surface, text_surface.get_rect(center=(x + w // 2, y + h // 2)))

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fondo
    screen.fill(GREENB)
    utils.draw_grid(pygame, screen, 50)

    # Dibujar elementos
    draw_betting_table()
    draw_special_rectangle()
    draw_external_bets()

    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
