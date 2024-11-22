import pygame
import os

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 2000, 1800
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

# Cargar las imágenes de las fichas (ajustadas a 10x10 píxeles)
chip_images = {
    'yellow': {
        5: pygame.image.load(os.path.join(image_folder, 'ficha_naranja_05.png')),
        10: pygame.image.load(os.path.join(image_folder, 'ficha_naranja_10.png')),
        20: pygame.image.load(os.path.join(image_folder, 'ficha_naranja_20.png')),
        50: pygame.image.load(os.path.join(image_folder, 'ficha_naranja_50.png')),
        100: pygame.image.load(os.path.join(image_folder, 'ficha_naranja_100.png'))
    },
    'blue': {
        5: pygame.image.load(os.path.join(image_folder, 'ficha_azul_05.png')),
        10: pygame.image.load(os.path.join(image_folder, 'ficha_azul_10.png')),
        20: pygame.image.load(os.path.join(image_folder, 'ficha_azul_20.png')),
        50: pygame.image.load(os.path.join(image_folder, 'ficha_azul_50.png')),
        100: pygame.image.load(os.path.join(image_folder, 'ficha_azul_100.png'))
    },
    'lilac': {
        5: pygame.image.load(os.path.join(image_folder, 'ficha_lila_05.png')),
        10: pygame.image.load(os.path.join(image_folder, 'ficha_lila_10.png')),
        20: pygame.image.load(os.path.join(image_folder, 'ficha_lila_20.png')),
        50: pygame.image.load(os.path.join(image_folder, 'ficha_lila_50.png')),
        100: pygame.image.load(os.path.join(image_folder, 'ficha_lila_100.png'))
    }
}

# Redimensionar las imágenes a 10x10 píxeles
for color in chip_images.values():
    for value in color.values():
        value = pygame.transform.scale(value, (10, 10))

# Organizar las posiciones de las fichas
chip_spacing = 20  # Espacio entre fichas
L_pos = [(100 + chip_spacing * i, 100) for i in range(5)]  # Posiciones para las fichas moradas
A_pos = [(100 + chip_spacing * i, 150) for i in range(5)]  # Posiciones para las fichas azules
N_pos = [(100 + chip_spacing * i, 200) for i in range(5)]  # Posiciones para las fichas naranjas

# Fichas y sus características
chips = [
    {'color': LILAC, 'values': [5, 10, 20, 50, 100], 'pos': L_pos, 'dragging': None, 'duplicated': []},
    {'color': BLUE, 'values': [5, 10, 20, 50, 100], 'pos': A_pos, 'dragging': None, 'duplicated': []},
    {'color': YELLOW, 'values': [5, 10, 20, 50, 100], 'pos': N_pos, 'dragging': None, 'duplicated': []}
]

# Función para dibujar las fichas (incluyendo las duplicadas)
def draw_chips():
    for chip in chips:
        for idx, value in enumerate(chip['values']):
            x, y = chip['pos'][idx]
            # Cargar y mostrar la imagen correspondiente
            chip_image = chip_images['lilac' if chip['color'] == LILAC else 'blue' if chip['color'] == BLUE else 'yellow'][value]
            screen.blit(chip_image, (x - chip_image.get_width() // 2, y - chip_image.get_height() // 2))

        # Dibuja las fichas duplicadas
        for duplicated_chip in chip['duplicated']:
            x, y = duplicated_chip['pos']
            chip_image = chip_images['lilac' if chip['color'] == LILAC else 'blue' if chip['color'] == BLUE else 'yellow'][duplicated_chip['value']]
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
            if dist < 15 and mouse_pressed[0]:
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

            # Si se hace clic en una ficha, duplicamos esa ficha
            if dist < 15 and mouse_pressed[0]:
                # Solo duplicamos si no hay fichas duplicadas
                if len(chip['duplicated']) == 0 or chip['duplicated'][-1]['value'] != value:
                    chip['duplicated'].append({'value': value, 'pos': (x, y)})

# Función principal para el bucle del juego
def main():
    running = True
    while running:
        screen.fill((0, 0, 0))  # Limpiar la pantalla

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
