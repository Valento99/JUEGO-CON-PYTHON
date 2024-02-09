import pygame
import random

pygame.init()

# Configuraciones de la pantalla
ancho_pantalla = 900
alto_pantalla = 600
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Esquivando Objetos")

# Colores
negro = (0, 0, 0)
verde = (0, 255, 0)
rojo = (255, 0, 0)

# Jugador
ancho_jugador = 30
alto_jugador = 30
posicion_x_jugador = ancho_pantalla // 2 - ancho_jugador // 2
posicion_y_jugador = alto_pantalla - alto_jugador - 10
velocidad_jugador = 8

# Disparos
disparos = []
ancho_disparo = 5
alto_disparo = 10
velocidad_disparo = 10

# Obstáculos
ancho_objeto = 50
alto_objeto = 50
velocidad_objeto = 5
objetos = []
tiempo_siguiente_objeto = 0
frecuencia_objetos = 150  # Reducir la frecuencia de generación de obstáculos

reloj = pygame.time.Clock()
jugando = True

# Puntaje y nivel
puntos = 0
fuente = pygame.font.Font(None, 36)
nivel = 1

# Menú de inicio con personalización
def mostrar_menu():
    fuente_menu = pygame.font.Font(None, 36)
    texto_menu = fuente_menu.render("ESQUIVANDO OBJETOS", True, verde)
    texto_personalizacion = fuente_menu.render("Escoge tu color [A: Amarillo, Z: Azul, R: Rojo]", True, verde)
    texto_forma = fuente_menu.render("Escoge tu forma [B: Bola, C: Cuadro, T: Triángulo]", True, verde)
    texto_instrucciones = fuente_menu.render("Presiona ESPACIO para empezar", True, verde)

    menu_activo = True
    color_jugador = (255, 0, 0)
    forma_jugador = 'cuadro'  # Por defecto, el jugador es un cuadro

    while menu_activo:
        pantalla.fill(negro)
        pantalla.blit(texto_menu, (ancho_pantalla // 2 - 200, alto_pantalla // 2 - 100))
        pantalla.blit(texto_instrucciones, (ancho_pantalla // 2 - 250, alto_pantalla // 2 + 50))
        pantalla.blit(texto_personalizacion, (ancho_pantalla // 2 - 250, alto_pantalla // 2))
        pantalla.blit(texto_forma, (ancho_pantalla // 2 - 250, alto_pantalla // 2 - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_activo = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return color_jugador, forma_jugador
                if event.key == pygame.K_a:
                    color_jugador = (255, 255, 0)  # Amarillo
                if event.key == pygame.K_z:
                    color_jugador = (0, 0, 255)  # Azul
                if event.key == pygame.K_r:
                    color_jugador = (255, 0, 0)  # Rojo
                if event.key == pygame.K_b:
                    forma_jugador = 'bola'
                if event.key == pygame.K_c:
                    forma_jugador = 'cuadro'
                if event.key == pygame.K_t:
                    forma_jugador = 'triangulo'

        pygame.display.update()

def dibujar_jugador(x, y, color, forma):
    if forma == 'cuadro':
        pygame.draw.rect(pantalla, color, (x, y, ancho_jugador, alto_jugador))
    elif forma == 'bola':
        pygame.draw.circle(pantalla, color, (x + ancho_jugador // 2, y + alto_jugador // 2), ancho_jugador // 2)
    elif forma == 'triangulo':
        puntos = [(x + ancho_jugador // 2, y), (x, y + alto_jugador), (x + ancho_jugador, y + alto_jugador)]
        pygame.draw.polygon(pantalla, color, puntos)

def mostrar_game_over():
    fuente_game_over = pygame.font.Font(None, 50)
    texto_game_over = fuente_game_over.render("¡Game Over!", True, verde)
    texto_puntuacion = fuente_game_over.render(f"Puntuación: {puntos}", True, verde)
    pantalla.blit(texto_game_over, (ancho_pantalla // 2 - 150, alto_pantalla // 2 - 50))
    pantalla.blit(texto_puntuacion, (ancho_pantalla // 2 - 150, alto_pantalla // 2))
    pygame.display.update()
    pygame.time.wait(2000)  # Espera 2 segundos antes de volver al menú

def reiniciar_variables():
    global objetos, puntos, nivel, velocidad_objeto
    objetos = []
    puntos = 0
    nivel = 1
    velocidad_objeto = 5

# Personalización del jugador desde el menú
color_elegido, forma_elegida = mostrar_menu()

# Colisiones entre disparos y obstáculos
def colisiones_disparos_objetos():
    for disparo in disparos:
        for objeto in objetos:
            if disparo.colliderect(objeto):
                disparos.remove(disparo)
                objetos.remove(objeto)
                return

while True:
    pantalla.fill(negro)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and posicion_x_jugador > 0:
        posicion_x_jugador -= velocidad_jugador
    if teclas[pygame.K_RIGHT] and posicion_x_jugador < ancho_pantalla - ancho_jugador:
        posicion_x_jugador += velocidad_jugador

    if pygame.time.get_ticks() > tiempo_siguiente_objeto:
        x = random.randrange(0, ancho_pantalla - ancho_objeto)
        y = -alto_objeto
        objetos.append(pygame.Rect(x, y, ancho_objeto, alto_objeto))
        tiempo_siguiente_objeto = pygame.time.get_ticks() + frecuencia_objetos

    for objeto in objetos:
        objeto.y += velocidad_objeto

    objetos = [obj for obj in objetos if obj.y < alto_pantalla]

    dibujar_jugador(posicion_x_jugador, posicion_y_jugador, color_elegido, forma_elegida)

    jugador_rect = pygame.Rect(posicion_x_jugador, posicion_y_jugador, ancho_jugador, alto_jugador)
    if any(jugador_rect.colliderect(objeto) for objeto in objetos):
        mostrar_game_over()
        reiniciar_variables()  # Reiniciar variables del juego
        color_elegido, forma_elegida = mostrar_menu()  # Volver al menú

    puntos += 1
    texto_puntos = fuente.render(f"Puntos: {puntos}", True, verde)
    pantalla.blit(texto_puntos, (10, 10))

    if puntos > 0 and puntos % 100 == 0:
        nivel += 1
        velocidad_objeto += 0.5

    # Manejo de disparos
    if teclas[pygame.K_x]:
        disparo = pygame.Rect(posicion_x_jugador + ancho_jugador // 2 - ancho_disparo // 2,
                              posicion_y_jugador - alto_disparo, ancho_disparo, alto_disparo)
        disparos.append(disparo)

    for disparo in disparos:
        disparo.y -= velocidad_disparo

    for disparo in disparos[:]:
        if disparo.y + alto_disparo < 0:
            disparos.remove(disparo)

    for objeto in objetos:
        pygame.draw.rect(pantalla, verde, objeto)

    for disparo in disparos:
        pygame.draw.rect(pantalla, rojo, disparo)

    colisiones_disparos_objetos()

    pygame.display.flip()
    reloj.tick(60)