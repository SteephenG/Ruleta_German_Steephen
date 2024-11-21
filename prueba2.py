import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ruleta")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Fuente para el texto
font = pygame.font.SysFont("Arial", 24)

# Datos de la ruleta (números de la ruleta con colores)
numbers = [
    (0, GREEN), (32, RED), (15, BLACK), (19, RED), (4, BLACK), (21, RED), (2, BLACK), (25, RED),
    (17, BLACK), (34, RED), (6, BLACK), (27, RED), (13, BLACK), (36, RED), (11, BLACK), (30, RED),
    (8, BLACK), (23, RED), (10, BLACK), (5, RED), (24, BLACK), (16, RED), (33, BLACK), (1, RED),
    (20, BLACK), (14, RED), (31, BLACK), (9, RED), (22, BLACK), (18, RED), (29, BLACK), (7, RED),
    (28, BLACK), (12, RED), (35, BLACK), (3, RED), (26, BLACK)
]

# Ángulo de rotación de la rueda
rotation_angle = 0
spin_speed = 0.2  # Velocidad del giro
spin_friction = 0.99  # Fricción para disminuir la velocidad al final del giro
spinning = False
target_number = None

# Función para dibujar la rueda
def draw_roulette():
    radius = 250
    center = (width // 2, height // 2)
    
    # Dibujar los sectores de la rueda
    for i, (num, color) in enumerate(numbers):
        angle = math.radians(i * (360 / len(numbers)) + rotation_angle)
        x1 = center[0] + math.cos(angle) * radius
        y1 = center[1] + math.sin(angle) * radius
        x2 = center[0] + math.cos(angle + math.radians(360 / len(numbers))) * radius
        y2 = center[1] + math.sin(angle + math.radians(360 / len(numbers))) * radius
        
        pygame.draw.polygon(screen, color, [center, (x1, y1), (x2, y2)])

        # Dibujar el número
        text = font.render(str(num), True, WHITE)
        text_rect = text.get_rect(center=(center[0] + math.cos(angle + math.radians(360 / len(numbers)) / 2) * (radius - 40),
                                          center[1] + math.sin(angle + math.radians(360 / len(numbers)) / 2) * (radius - 40)))
        screen.blit(text, text_rect)

# Función para dibujar la bola
def draw_ball():
    ball_radius = 15
    ball_x = width // 2 + math.cos(math.radians(rotation_angle)) * 220
    ball_y = height // 2 + math.sin(math.radians(rotation_angle)) * 220
    pygame.draw.circle(screen, YELLOW, (int(ball_x), int(ball_y)), ball_radius)

# Función para girar la rueda
def spin_roulette():
    global rotation_angle, spin_speed, spinning, target_number
    if spinning:
        rotation_angle += spin_speed
        spin_speed *= spin_friction  # Aplicar fricción para desacelerar la rueda
        if spin_speed < 0.02:  # La rueda se detiene cuando la velocidad es suficientemente baja
            spinning = False
            target_number = (int(rotation_angle // (360 / len(numbers))) % len(numbers))  # Número objetivo
            print(f"La bola cayó en el número: {numbers[target_number][0]} ({'ROJO' if numbers[target_number][1] == RED else 'NEGRO' if numbers[target_number][1] == BLACK else 'VERDE'})")
    
# Bucle principal
running = True
while running:
    screen.fill(WHITE)

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Iniciar el giro con la barra espaciadora
                if not spinning:
                    spinning = True
                    spin_speed = 10  # Velocidad inicial del giro

    # Dibujar la rueda
    draw_roulette()
    
    # Dibujar la bola
    if spinning:
        draw_ball()
    else:
        if target_number is not None:
            pygame.draw.circle(screen, YELLOW, (width // 2, height // 2), 10)  # Marca el centro cuando para

    # Hacer girar la ruleta
    spin_roulette()

    # Actualizar pantalla
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
