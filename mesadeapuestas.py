import pygame
import utils
# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 1100, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mesa de Apuestas - Ruleta de Casino")

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (169, 169, 169)
DARK_RED = (139, 0, 0)
DARK_BLACK = (50, 50, 50)
GREENF = (53, 131, 61, 1)
GREENB= (77, 115, 61, 1)



# Fuente para el texto
font = pygame.font.SysFont("Times New Roman", 23)


# Datos de la mesa de apuestas (en formato horizontal)
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
    
    cell_width = 50
    cell_height = 50
    offset_x = 250
    offset_y = 450

    # Dibujar el número 0 apartado (en la parte superior centrado)
    'zero_x = offset_x - 2 * cell_width  # Colocado a la izquierda, apartado'
    'zero_y = offset_y - 2 * cell_height  # Separado de las filas'
    'pygame.draw.rect(screen, GREEN, (zero_x, zero_y, cell_width, cell_height))'
    'pygame.draw.rect(screen, WHITE, (zero_x, zero_y, cell_width, cell_height), width=2)'
    'text_surface = font.render("0", True, WHITE)'
    'screen.blit(text_surface, text_surface.get_rect(center=(zero_x + cell_width // 2, zero_y + cell_height // 2)))'

    # Dibujar números (disposición horizontal)
    for i, row in enumerate(numbers):
        for j, num in enumerate(row):
            x = offset_x + j * cell_width
            y = offset_y + (i * cell_height)

            # Dibujar celda
            color = colors.get(num, GRAY)
            pygame.draw.rect(screen, color, (x, y, cell_width, cell_height))
            pygame.draw.rect(screen, WHITE, (x, y, cell_width, cell_height), width=2)

            # Dibujar texto
            text_surface = font.render(str(num), True, WHITE)
            screen.blit(text_surface, text_surface.get_rect(center=(x + cell_width // 2, y + cell_height // 2)))

    # Apuestas externas: Colocamos las apuestas fuera de la mesa principal, debajo
    external_bets = [
        # "1st 12" (debajo de los números 1 a 12)
        ("1st 12", offset_x, offset_y + len(numbers) * cell_height + 40, 4),
        ("1 to 18", offset_x, offset_y + len(numbers) * cell_height + 90, 2),
        ("PAR", offset_x + 2 * cell_width, offset_y + len(numbers) * cell_height + 90, 2),

        # "2nd 12" (debajo de los números 13 a 24)
        ("2nd 12", offset_x + 4 * cell_width, offset_y + len(numbers) * cell_height + 40, 4),
        ("ROJAS", offset_x + 4 * cell_width, offset_y + len(numbers) * cell_height + 90, 2),
        ("NEGRAS", offset_x + 6 * cell_width, offset_y + len(numbers) * cell_height + 90, 2),

        # "3rd 12" (debajo de los números 25 a 36)
        ("3rd 12", offset_x + 8 * cell_width, offset_y + len(numbers) * cell_height + 40, 4),
        ("IMPAR", offset_x + 8 * cell_width, offset_y + len(numbers) * cell_height + 90, 2),
        ("19 to 36", offset_x + 10 * cell_width, offset_y + len(numbers) * cell_height + 90, 2),
    ]

    # Dibujar apuestas externas
    for bet, x, y, *width_mult in external_bets:
        w = cell_width * (width_mult[0] if width_mult else 2)
        h = cell_height

        if bet == "ROJAS":
            color = DARK_RED
        elif bet == "NEGRAS":
            color = DARK_BLACK
        else:
            color = LIGHT_GRAY  # Usar un color estándar para otras apuestas
        pygame.draw.rect(screen, color, (x, y, w, h))
        pygame.draw.rect(screen, WHITE, (x, y, w, h), width=2)

        text_surface = font.render(bet, True, BLACK)
        screen.blit(text_surface, text_surface.get_rect(center=(x + w // 2, y + h // 2)))


# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    # Fondo
    screen.fill(GREENF)

    pygame.draw.rect(screen, GREENB, (150, 450, 100, 150),)
    pygame.draw.rect(screen, WHITE, (150, 450, 100, 150), 4)
   
    text = font.render('0', True, WHITE)
    rotated_text = pygame.transform.rotate(text, 90)
    # Obtener el rectángulo del texto rotado para posicionarlo correctamente
    rotated_rect = rotated_text.get_rect(center=(205, 525))
    # Dibujar el número rotado en la pantalla
    screen.blit(rotated_text, rotated_rect)
    # Dibujar mesa de apuestas
    draw_betting_table()

    # Actualizar pantalla
    pygame.display.flip()
pygame.quit()
