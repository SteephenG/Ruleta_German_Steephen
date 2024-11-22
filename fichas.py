import pygame
import os

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fichas de Casino")

# Colores
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LILAC = (200, 162, 200)
BLACK = (0, 0, 0)

# Fuente para texto
font = pygame.font.SysFont(None, 30)

# Ruta de las imágenes de las fichas
image_folder = os.path.join(os.path.dirname(__file__), "Imagenes/fichas")

# Función para cargar y redimensionar las imágenes de las fichas
def load_chip_image(file_name):
    image = pygame.image.load(os.path.join(image_folder, file_name))
    return pygame.transform.scale(image, (60, 60))  # Redimensionamos a 60x60 píxeles

# Cargar las imágenes de las fichas
chip_images = {
    'yellow': {
        5: load_chip_image('ficha_naranja_05.png'),
        10: load_chip_image('ficha_naranja_10.png'),
        20: load_chip_image('ficha_naranja_20.png'),
        50: load_chip_image('ficha_naranja_50.png'),
        100: load_chip_image('ficha_naranja_100.png')
    },
    'blue': {
        5: load_chip_image('ficha_azul_05.png'),
        10: load_chip_image('ficha_azul_10.png'),
        20: load_chip_image('ficha_azul_20.png'),
        50: load_chip_image('ficha_azul_50.png'),
        100: load_chip_image('ficha_azul_100.png')
    },
    'lilac': {
        5: load_chip_image('ficha_lila_05.png'),
        10: load_chip_image('ficha_lila_10.png'),
        20: load_chip_image('ficha_lila_20.png'),
        50: load_chip_image('ficha_lila_50.png'),
        100: load_chip_image('ficha_lila_100.png')
    }
}

# Fichas y sus características
chips = [
    {'color': YELLOW, 'values': [5, 10, 20, 50, 100], 'pos': [(100, 100), (200, 100), (300, 100), (400, 100), (500, 100)], 'dragging': None, 'duplicated': [], 'limits': {5: 3, 10: 3, 20: 3, 50: 3, 100: 3}},
    {'color': BLUE, 'values': [5, 10, 20, 50, 100], 'pos': [(100, 200), (200, 200), (300, 200), (400, 200), (500, 200)], 'dragging': None, 'duplicated': [], 'limits': {5: 3, 10: 3, 20: 3, 50: 3, 100: 3}},
    {'color': LILAC, 'values': [5, 10, 20, 50, 100], 'pos': [(100, 300), (200, 300), (300, 300), (400, 300), (500, 300)], 'dragging': None, 'duplicated': [], 'limits': {5: 3, 10: 3, 20: 3, 50: 3, 100: 3}},
]

# Función para dibujar las fichas (incluyendo las duplicadas y el contador)
def draw_chips():
    for chip in chips:
        for idx, value in enumerate(chip['values']):
            x, y = chip['pos'][idx]
            # Cargar y mostrar la imagen correspondiente
            chip_image = chip_images['yellow' if chip['color'] == YELLOW else 'blue' if chip['color'] == BLUE else 'lilac'][value]
            screen.blit(chip_image, (x - chip_image.get_width() // 2, y - chip_image.get_height() // 2))
            
            # Mostrar la cantidad de fichas disponibles al lado
            limit_text = f"x{chip['limits'][value]}"
            text_surface = font.render(limit_text, True, BLACK)
            screen.blit(text_surface, (x + chip_image.get_width() // 2 + 10, y - text_surface.get_height() // 2))

        # Dibuja las fichas duplicadas
        for duplicated_chip in chip['duplicated']:
            x, y = duplicated_chip['pos']
            chip_image = chip_images['yellow' if chip['color'] == YELLOW else 'blue' if chip['color'] == BLUE else 'lilac'][duplicated_chip['value']]
            screen.blit(chip_image, (x - chip_image.get_width() // 2, y - chip_image.get_height() // 2))

# Función para manejar el arrastre de las fichas duplicadas
def handle_chip_drag():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for chip in chips:
        for idx, value in enumerate(chip['values']):
            x, y = chip['pos'][idx]
            dist = ((x - mouse_x) ** 2 + (y - mouse_y) ** 2) ** 0.5  # Distancia entre la ficha y el mouse

            # Si la ficha es clickeada, empieza a ser arrastrada
            if dist < 30 and mouse_pressed[0]:
                chip['dragging'] = idx  # Guardamos el índice de la ficha que estamos arrastrando
                chip['drag_offset'] = (x - mouse_x, y - mouse_y)  # Guardamos el desplazamiento desde el click

        # Si estamos arrastrando una ficha, movemos la posición de la ficha duplicada
        for duplicated_chip in chip['duplicated']:
            if chip['dragging'] is not None:
                if mouse_pressed[0]:
                    duplicated_chip['pos'] = (mouse_x + chip['drag_offset'][0], mouse_y + chip['drag_offset'][1])

        # Si soltamos el botón, la ficha deja de ser arrastrada
        if not mouse_pressed[0]:
            chip['dragging'] = None

# Función para manejar la creación de fichas duplicadas al hacer clic
def handle_chip_creation():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for chip in chips:
        for idx, value in enumerate(chip['values']):
            x, y = chip['pos'][idx]
            dist = ((x - mouse_x) ** 2 + (y - mouse_y) ** 2) ** 0.5  # Distancia entre la ficha y el mouse

            # Solo permitir duplicar si no está siendo arrastrada, hay fichas disponibles y el clic fue en una ficha con límite > 0
            if dist < 30 and mouse_pressed[0] and chip['dragging'] is None:
                if chip['limits'][value] > 0:  # Comprobamos que hay fichas disponibles
                    # Crear una nueva ficha duplicada
                    chip['duplicated'].append({'value': value, 'pos': (x, y)})
                    chip['limits'][value] -= 1  # Reducir el contador de fichas disponibles

# Función principal para el bucle del juego
def main():
    running = True
    while running:
        screen.fill((255, 255, 255))  # Limpiar la pantalla

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_chip_creation()
        handle_chip_drag()
        draw_chips()

        pygame.display.update()  # Actualizar la pantalla
        pygame.time.Clock().tick(60)  # FPS

    pygame.quit()

if __name__ == "__main__":
    main()
