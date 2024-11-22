import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Casino Online: Arrastrar Fichas")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar la imagen de la ficha (suponiendo que tienes una imagen de ficha llamada "chip.png")
chip_image = pygame.image.load('Imagenes/ficha_azul_100')  # Asegúrate de tener la imagen 'chip.png'

# Redimensionar la imagen para que sea más pequeña (ajustando el tamaño a la mitad, por ejemplo)
chip_width, chip_height = chip_image.get_size()
new_width = chip_width // 2  # Reducir al 50% del tamaño original
new_height = chip_height // 2  # Reducir al 50% del tamaño original
chip_image = pygame.transform.scale(chip_image, (new_width, new_height))  # Redimensionar la imagen

chip_rect = chip_image.get_rect()

# Lista de fichas apiladas
chips = []

# Variables para arrastrar fichas
dragging_chip = None
drag_offset = (0, 0)

# Función para crear fichas apiladas
def create_stacked_chips(x, y, count):
    """Genera varias fichas apiladas una encima de la otra."""
    chips.clear()  # Limpiar cualquier ficha anterior
    for i in range(count):
        chip = {
            'image': chip_image,
            'rect': chip_image.get_rect(topleft=(x, y + i * 40))  # Desplazamiento de 10px por ficha
        }
        chips.append(chip)

# Función para arrastrar las fichas
def drag_chip():
    global dragging_chip, drag_offset
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if dragging_chip:
        # Mover la ficha arrastrada
        dragging_chip['rect'].topleft = (mouse_x - drag_offset[0], mouse_y - drag_offset[1])

def handle_events():
    global dragging_chip, drag_offset

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for chip in chips:
                if chip['rect'].collidepoint(event.pos):
                    # Iniciar arrastre de la ficha
                    dragging_chip = chip
                    drag_offset = (event.pos[0] - chip['rect'].x, event.pos[1] - chip['rect'].y)
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            # Detener el arrastre
            dragging_chip = None

    return True

# Bucle principal
running = True

# Crear las fichas amontonadas
create_stacked_chips(300, 300, 5)  # Crear 5 fichas apiladas en la posición (300, 300)

while running:
    running = handle_events()

    # Fondo de pantalla
    screen.fill(WHITE)

    # Dibujar fichas apiladas
    for chip in chips:
        screen.blit(chip['image'], chip['rect'])

    # Arrastrar la ficha seleccionada
    drag_chip()

    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
