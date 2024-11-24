import pygame
import os

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 1920, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Casino con Jugadores y Fichas")

# Colores
TARONJA = (255, 165, 0)
LILA = (138, 43, 226)
BLAU = (0, 0, 255)

# Cargar imágenes de las fichas desde la carpeta 'imagenes'
# Redimensionamos las fichas a 50x50 píxeles
fichas_azul = [pygame.transform.scale(pygame.image.load(os.path.join('imagenes', f'ficha_azul_{v}.png')), (50, 50)) for v in [5, 10, 20, 50, 100]]
fichas_naranja = [pygame.transform.scale(pygame.image.load(os.path.join('imagenes', f'ficha_naranja_{v}.png')), (50, 50)) for v in [5, 10, 20, 50, 100]]
fichas_lila = [pygame.transform.scale(pygame.image.load(os.path.join('imagenes', f'ficha_lila_{v}.png')), (50, 50)) for v in [5, 10, 20, 50, 100]]

# Variables de jugadores y sus fichas
jugadores = {
    'Taronja': {'color': TARONJA, 'fichas': [2, 1, 1, 1, 0]},  # 005, 010, 020, 050, 100
    'Lila': {'color': LILA, 'fichas': [2, 2, 1, 0, 0]},
    'Blau': {'color': BLAU, 'fichas': [2, 1, 2, 1, 0]},
}

# Clase para representar cada ficha
class Ficha:
    def __init__(self, valor, imagen, jugador_nombre):
        self.valor = valor
        self.imagen = imagen
        self.jugador_nombre = jugador_nombre
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (0, 0)
        self.agarrada = False  # Para saber si está siendo arrastrada

# Crear las fichas de los jugadores
fichas_taronja = [Ficha(5, fichas_naranja[0], 'Taronja'), Ficha(10, fichas_naranja[1], 'Taronja'), Ficha(20, fichas_naranja[2], 'Taronja'), Ficha(50, fichas_naranja[3], 'Taronja'), Ficha(100, fichas_naranja[4], 'Taronja')]
fichas_lila = [Ficha(5, fichas_lila[0], 'Lila'), Ficha(10, fichas_lila[1], 'Lila'), Ficha(20, fichas_lila[2], 'Lila'), Ficha(50, fichas_lila[3], 'Lila'), Ficha(100, fichas_lila[4], 'Lila')]
fichas_blau = [Ficha(5, fichas_azul[0], 'Blau'), Ficha(10, fichas_azul[1], 'Blau'), Ficha(20, fichas_azul[2], 'Blau'), Ficha(50, fichas_azul[3], 'Blau'), Ficha(100, fichas_azul[4], 'Blau')]

# Crear una lista global con todas las fichas
fichas = fichas_taronja + fichas_lila + fichas_blau

# Configuración de la fuente
font = pygame.font.SysFont("Arial", 20)

# Variables globales
ficha_arrastrada = None  # Ficha que está siendo arrastrada
posicion_inicial_ficha = None  # Posición inicial de la ficha antes de ser arrastrada

# Función para dibujar las fichas y el contador de fichas
def dibujar_fichas():
    offset_y = 100
    separacion = 60  # Separación de 60px entre fichas
    for i, ficha in enumerate(fichas):
        # Disposición horizontal (una fila)
        ficha.rect.topleft = (50 + i * separacion, offset_y)
        screen.blit(ficha.imagen, ficha.rect.topleft)

        # Mostrar el contador de fichas
        cantidad = jugadores[ficha.jugador_nombre]['fichas'][fichas.index(ficha) % 5]  # Accedemos por nombre del jugador
        texto = font.render(f"x{cantidad}", True, (255, 255, 255))
        screen.blit(texto, (ficha.rect.x + 35, ficha.rect.y + 5))  # Ajuste de la posición del contador

# Función para manejar el arrastre de las fichas
def manejar_arrastre():
    global ficha_arrastrada, posicion_inicial_ficha

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_presionado = pygame.mouse.get_pressed()[0]  # Verifica si el mouse está presionado

    # Si hay una ficha arrastrada, la mostramos en la nueva posición del mouse
    if ficha_arrastrada:
        screen.blit(ficha_arrastrada.imagen, (mouse_x - ficha_arrastrada.imagen.get_width() // 2, mouse_y - ficha_arrastrada.imagen.get_height() // 2))

    # Si no estamos arrastrando ninguna ficha, verificamos si se hace clic en alguna
    if not ficha_arrastrada:
        for ficha in fichas:
            if ficha.rect.collidepoint(mouse_x, mouse_y) and jugadores[ficha.jugador_nombre]['fichas'][fichas.index(ficha) % 5] > 0:
                if mouse_presionado:  # Si el mouse está presionado, iniciamos el arrastre
                    ficha_arrastrada = ficha
                    posicion_inicial_ficha = ficha.rect.topleft

    # Si el mouse se suelta y estamos arrastrando una ficha, la soltamos
    if not mouse_presionado and ficha_arrastrada:
        jugadores[ficha_arrastrada.jugador_nombre]['fichas'][fichas.index(ficha_arrastrada) % 5] -= 1
        ficha_arrastrada = None  # Dejamos de arrastrar la ficha

# Bucle principal
running = True
while running:
    screen.fill((0, 0, 0))  # Fondo negro
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Llamamos a las funciones de dibujo y arrastre
    dibujar_fichas()  # Mostrar las fichas y los contadores
    manejar_arrastre()  # Controlar el arrastre de las fichas

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
