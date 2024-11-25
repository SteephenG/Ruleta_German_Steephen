import pygame
import os

# Inicialización de Pygame
pygame.init()

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
    'Naranja': {'fichas': [2, 1, 1, 1, 0]},
    'Lila': {'fichas': [2, 2, 1, 0, 0]},
    'Azul': {'fichas': [2, 1, 2, 1, 0]},
}

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
            imagen = pygame.transform.scale(pygame.image.load(ruta_imagen), (50, 50))
            fichas_jugador.append(Ficha(valor, imagen, jugador))
        fichas.extend(fichas_jugador)
    return fichas

# Dibujar las fichas en pantalla
def dibujar_fichas(fichas, fuente):
    offset_y = 100
    separacion = 60
    for i, ficha in enumerate(fichas):
        ficha.rect.topleft = (50 + i * separacion, offset_y)
        pantalla.blit(ficha.imagen, ficha.rect.topleft)

        # Mostrar cantidad restante
        cantidad = JUGADORES[ficha.jugador_nombre]['fichas'][VALORES_FICHAS.index(ficha.valor)]
        texto = fuente.render(f"x{cantidad}", True, (255, 255, 255))
        pantalla.blit(texto, (ficha.rect.x + 35, ficha.rect.y + 5))

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
corriendo = True
while corriendo:
    pantalla.fill((0, 0, 0))
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    dibujar_fichas(fichas, fuente)
    manejar_arrastre(fichas)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
