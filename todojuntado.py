import pygame
import math
import random
import os
import utils

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
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#RULETA
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

    
#
#
#
#
#
#
#
#
#

##
#

#
#
#
#
#
#
#
#
#
#MESA DE APUESTAS
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
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

# Configuración de la pantalla
ANCHO, ALTO = 1920, 900
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Casino con Jugadores y Fichas")

# Colores
COLORES = {
    'Naranja': (255, 165, 0),
    'Lila': (138, 43, 226),
    'Azul': (0, 0, 255),
}

# Configuración de jugadores y fichas
VALORES_FICHAS = [5, 10, 20, 50, 100]
JUGADORES = {
    'Naranja': {'fichas': [2, 2, 1, 0, 0]},
    'Lila': {'fichas': [2, 2, 1, 0, 0]},
    'Azul': {'fichas': [2, 2, 1, 0, 0]},
}

def calcular_dinero(jugador):
    fichas = JUGADORES[jugador]['fichas']
    dinero = sum(fichas[i] * VALORES_FICHAS[i] for i in range(len(fichas)))
    return dinero

dinero_jugadores = {jugador: calcular_dinero(jugador) for jugador in JUGADORES}


# Clase para las fichas
class Ficha:
    def __init__(self, valor, imagen, jugador_nombre):
        self.valor = valor
        self.imagen = imagen
        self.jugador_nombre = jugador_nombre
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (0, 0)
        self.agarrada = False

# Función para cargar imágenes de fichas
def cargar_fichas():
    fichas = []
    for jugador, datos in JUGADORES.items():
        fichas_jugador = []
        for valor in VALORES_FICHAS:
            ruta_imagen = os.path.join('Imagenes', f'ficha_{jugador.lower()}_{valor}.png')
            imagen = pygame.transform.scale(pygame.image.load(ruta_imagen), (70, 70))
            fichas_jugador.append(Ficha(valor, imagen, jugador))
        fichas.extend(fichas_jugador)
    return fichas

# Dibujar las fichas en pantalla
def dibujar_fichas(fichas, fuente):
    offset_y = 800
    offset_x = 800  # Este es el valor base para la posición x
    separacion = 70  # La separación entre las fichas

    for i, ficha in enumerate(fichas):
        # Establecer una nueva posición x basada en el índice (i)
        ficha.rect.topleft = (offset_x + i * separacion, offset_y)

        # Dibujar la ficha
        pantalla.blit(ficha.imagen, ficha.rect.topleft)

        # Mostrar la cantidad restante de fichas
        cantidad = JUGADORES[ficha.jugador_nombre]['fichas'][VALORES_FICHAS.index(ficha.valor)]
        texto = fuente.render(f"x{cantidad}", True, (255, 255, 255))
        pantalla.blit(texto, (ficha.rect.x + 25, ficha.rect.y + 70))


# Manejo del arrastre de fichas
def manejar_arrastre(fichas):
    global ficha_arrastrada, posicion_inicial_ficha

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_presionado = pygame.mouse.get_pressed()[0]

    if ficha_arrastrada:
        pantalla.blit(ficha_arrastrada.imagen, (mouse_x - ficha_arrastrada.imagen.get_width() // 2,
                                                mouse_y - ficha_arrastrada.imagen.get_height() // 2))

    if not ficha_arrastrada:
        for ficha in fichas:
            if ficha.rect.collidepoint(mouse_x, mouse_y):
                indice = VALORES_FICHAS.index(ficha.valor)
                if JUGADORES[ficha.jugador_nombre]['fichas'][indice] > 0 and mouse_presionado:
                    ficha_arrastrada = ficha
                    posicion_inicial_ficha = ficha.rect.topleft

    if not mouse_presionado and ficha_arrastrada:
        indice = VALORES_FICHAS.index(ficha_arrastrada.valor)
        JUGADORES[ficha_arrastrada.jugador_nombre]['fichas'][indice] -= 1
        ficha_arrastrada = None

# Inicialización de variables
fichas = cargar_fichas()
fuente = pygame.font.SysFont("Arial", 20)
ficha_arrastrada = None
posicion_inicial_ficha = None

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

    # Dibujar la ruleta y la mesa de apuestas
    draw_roulette()
    draw_arrow()
    draw_betting_table()
    dibujar_fichas(fichas, font)  # Dibujar las fichas
    manejar_arrastre(fichas)  # Manejar el arrastre de las fichas
    
    pygame.display.flip()  # Actualizar la pantalla

    # Control de framerate
    pygame.time.Clock().tick(60)

pygame.quit()
