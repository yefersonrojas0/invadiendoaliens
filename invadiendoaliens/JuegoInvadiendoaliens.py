import pygame
import sys
import random
import time

import pygame.mixer
import pygame.mixer_music
 
# Inicializar Pygame y mixer
pygame.init()
pygame.mixer.init()
 
# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("INVADIENDO ALIENS")
 
# Colores
red_misil = (200, 25, 0)
 
#Jugador
jugador_width = 60
jugador_height = 60
jugador_x = width // 2 - jugador_width // 2
jugador_y = height - jugador_height - 10
jugador_speed = 8
 
#Enemigo 
enemy_width = 60
enemy_height = 60
enemy_speed = 1
enemys = []
previous_enemy_speed = 0  
 
#Bala
misil_width = 3
misil_height = 10
misil_speed = 10
misiles = []
 
#Niveles
current_level = 1
count_killers= 0
max_levels = 3

#Cargando Imagenes Jugador , enemigo , Fondo y inicio
jugador_image = pygame.image.load("player.png")
jugador_image = pygame.transform.scale(jugador_image, (jugador_width, jugador_height))
 
enemies = pygame.image.load("enemy.png")
enemies = pygame.transform.scale(enemies, (enemy_width, enemy_height))
 
wall = pygame.image.load("wall2.png")
wall = pygame.transform.scale(wall, (width,height))

start_image = pygame.image.load("imagen1-p.jpg")
start_image = pygame.transform.scale(start_image, (width, height))
 
# Configuración del cronómetro
start_time = pygame.time.get_ticks()
elapsed_time = 0

#configuracion del parpadeo del espacio
tiempo_actual_parpadeo = pygame.time.get_ticks()
intervalo_parpadeo = 1000
ultimo_parpadeo = pygame.time.get_ticks()
mensaje_visible = True

#configuracion del disparo 
tecla_espacio_presionada = False

#FUENTES DE ESCRITURA

#fuente de espacio comenzar 
fuente_pixeleada = pygame.font.Font("./PressStart2P-Regular.ttf", 14)
mensaje = fuente_pixeleada.render("Presiona ESPACIO para continuar", True, (255,255,255))
#fuente de nivel y puntos
font = pygame.font.SysFont(None, 40) #Fuente para el texto

#fuente del cronometro
timer_font = pygame.font.Font(None, 36)

# fuentes para mostrar en la pantalla(Display)

#fuente de game over
font_text = pygame.font.Font("./PressStart2P-Regular.ttf", 70)
#fuente del titulo
font_text1 = pygame.font.Font('./RubikBrokenFax-Regular.ttf', 45)
#fuente de lo que se muestra al final
font_text2 = pygame.font.Font ("./PressStart2P-Regular.ttf", 13)


#sonido y musica

disparo_sound = pygame.mixer.Sound('./laser.wav')
disparo_sound.set_volume(0.1)

finish_sound = pygame.mixer.Sound ('./audiofinish.wav')
nivel_sound = pygame.mixer.Sound ('./Nivel.wav')
nivel_sound.set_volume(0.3)

#musica level 1
level1_sound = pygame.mixer.Sound('./level1.wav')
level1_sound.set_volume(0.7)

#musica level 2

level2_sound = pygame.mixer.Sound('./level2.wav')
level2_sound.set_volume(0.5)

#musica level 3
level3_sound = pygame.mixer.Sound('./musicjuego.wav')
level3_sound.set_volume(0.4)

#musica inicio
pygame.mixer_music.load('./Grabación (7).mp3 ',) #musica del inicio

#sonido game over
gameover_sound = pygame.mixer.Sound ('./gameover.wav')



# Definir límites máximos para enemy_speed según el nivel
enemy_speed_inicial = {
    1: 0,
    2: 2.5,
    3: 5.0,
}

enemy_speed_limits = {
    1:2.5,
    2:5.0,
    3:10.0
    
}

enemy_speed_max = 10.0


#esto era para acomodar la hitbox de los enemigos
def get_misil_hitbox(misil):
    return pygame.Rect(misil['x']  -5 , misil['y'] - 5, misil_width + 10, misil_height + 10)
 
def colisiones_balas():
    global count_killers, misiles, enemys, enemy_speed, enemy_speed_max

    misiles_to_remover = []
    enemys_to_remover = []

    for misil in misiles[:]:
        for enemy in enemys[:]:
            misil_hitbox = get_misil_hitbox(misil)
            enemy_hitbox = pygame.Rect(enemy['x'] + 18, enemy['y'] + 15, enemy_width - 35, enemy_height - 35)

            if misil_hitbox.colliderect(enemy_hitbox):
                count_killers += 1
                enemy_speed += 0.1

                if current_level == 1:
                    enemy_speed_max = enemy_speed_limits.get(1, 2.5)
                    print(enemy_speed)
                    if enemy_speed > enemy_speed_max:
                        enemy_speed = enemy_speed_max
                elif current_level == 2:
                    enemy_speed_max = enemy_speed_limits.get(2, 5.0)
                    print(enemy_speed)
                    if enemy_speed > enemy_speed_max:
                        enemy_speed = enemy_speed_max
                elif current_level == 3:
                    enemy_speed_max = enemy_speed_limits.get(3, 10.0)
                    print(enemy_speed)
                    if enemy_speed > enemy_speed_max:
                        enemy_speed = enemy_speed_max

                print("Colisión detectada. Eliminando bala y monstruo.")
                print("misil:", misil)
                print("enemy:", enemy)

                misiles_to_remover.append(misil)
                enemys_to_remover.append(enemy)
                crear_enemigo1()
                
    
    # Eliminar monstruos de la lista
    misiles = [misil for misil in misiles if misil not in misiles_to_remover]
    enemys = [enemy for enemy in enemys if enemy not in enemys_to_remover]

#para crea solo un enemigo cuando se necesite
def crear_enemigo1():
    x = random.randint(0, 800)
    y = random.randint(-4000, -50)
    enemys.append({'x': x, 'y': y})

#crear enemigos dependiendo de nivel
def crear_enemigo(nivel):
    global enemys, width, height

    # Determina la cantidad de enemigos basándote en el nivel
    if nivel == 1:
        cantidad_enemigos = 50
    elif nivel == 2:
        cantidad_enemigos = 60
    elif nivel == 3:
        cantidad_enemigos = 70
    else:
        cantidad_enemigos = 0

    # Crea los enemigos
    for i in range(cantidad_enemigos):
        x = random.randint(0, width)
        y = random.randint(-4000, -50)
        enemys.append({'x': x, 'y': y})
        
def dibujar():
        
        # Dibujar balas
        for misil in misiles:
            pygame.draw.rect(screen, red_misil, [misil['x'], misil['y'], misil_width, misil_height])
            
        # crear monstruos y el jugador esta en la lista enemys
        for enemy in enemys:
            screen.blit(enemies, (enemy["x"], enemy["y"]))
            screen.blit(jugador_image, (jugador_x, jugador_y))

def disparo():
    global tecla_espacio_presionada
    teclas = pygame.key.get_pressed()
   
    if teclas[pygame.K_SPACE] and not tecla_espacio_presionada:
        misiles.append({'x': jugador_x + jugador_width // 2 - misil_width // 2, 'y': jugador_y}) 
        misiles.append({'x': jugador_x + jugador_width // 2 - misil_width // 2, 'y': jugador_y})
        disparo_sound.play()
        tecla_espacio_presionada = True
    elif not teclas[pygame.K_SPACE]:
        tecla_espacio_presionada = False            
                         
def entrada_juego():
 
    global jugador_x,jugador_y, current_level
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
 
    teclas = pygame.key.get_pressed()
    
    #Movimiento de la nave
    if teclas[pygame.K_RIGHT] and jugador_x < width - jugador_width:
            jugador_x += jugador_speed
    elif teclas[pygame.K_LEFT] and jugador_x > 0 :
            jugador_x -= jugador_speed
        
def colisiones_enemigo():
    # Colisión del jugador con los monstruos
    for enemy in enemys:
        # Ajustar los límites de colisión para el jugador
        jugador_hitbox = pygame.Rect(jugador_x + 17, jugador_y + 5, jugador_width - 35, jugador_height - 25)
        enemy_hitbox = pygame.Rect(enemy['x'] + 18, enemy['y'] + 15, enemy_width - 35, enemy_height - 35)

        # Verificar colisión
        if jugador_hitbox.colliderect(enemy_hitbox):
            level3_sound.stop()
            level1_sound.stop()
            level2_sound.stop()
            gameover_sound.play()
            display_message("GAME OVER")
            pygame.quit()
            sys.exit()
                
def mover_misiles():
    global misiles
    
    for misil in misiles:
            misil['y'] -= misil_speed
    
    #Eliminar balas que han salido de la pantalla
    misiles = [misil for misil in misiles if misil['y'] > 0] 
 
def mover_enemys():
    global enemys,current_time
 
    # mover monstruos y crear nuevos cuando salgan de la pantalla
    for enemy in enemys:
        enemy['y'] += enemy_speed   #current_time / 5000
        if enemy['y'] > height:
            enemys.remove(enemy)
            crear_enemigo1()

def cronómetro():
    global current_time,elapsed_time,remaining_seconds, minutes, seconds
    
     # Calcular el tiempo transcurrido
    current_time = pygame.time.get_ticks()
  
    elapsed_time = current_time - start_time
 
    # Calcular minutos y segundos restantes
    remaining_seconds = max(0, 60 - elapsed_time // 1000)
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
 
    # Formatear el tiempo restante como "minutos:segundos"
    time_str = "{:02}:{:02}".format(minutes, seconds)
 
    # Mostrar el tiempo restante
    timer_text = timer_font.render(f"Tiempo: {time_str}", True, (255,255,255))
    screen.blit(timer_text, (610, 15))
    
    if remaining_seconds == 0:
        iniciar_new_nivel()
 
    #La funcion retorna el tiempo
    return current_time
    
def clean_display():
    
    level_text = font.render(f"Nivel: {current_level}", True, (255, 255, 255))
    score_text = font.render(f"Puntos: {count_killers}", True, (255, 255, 255))     
    
    screen.blit(wall, (0, 0))
    screen.blit(level_text, (10, 10))
    screen.blit(score_text, (10, 40))

def inicio():
    global screen

    # Mostrar la imagen de inicio
    screen.blit(start_image, (0, 0))
    
    # Mostrar el título del juego
    title_font = pygame.font.Font('./RubikBrokenFax-Regular.ttf', 70) 
    title_text = title_font.render("INVADIENDO ALIENS", True, (255, 255, 255))
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 100))
    
    pygame.display.flip()
 
def reiniciar_cronometro():
    global elapsed_time, timer_font, start_time
    elapsed_time = 0
    start_time = pygame.time.get_ticks()   
   
def esperar_inicio():
    global esperando_inicio, mensaje_visible, tiempo_actual_parpadeo, ultimo_parpadeo, intervalo_parpadeo, mensaje
    
    pygame.mixer_music.play(-1)
    
    while esperando_inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
           
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                esperando_inicio = False
                reiniciar_cronometro()
                
        tiempo_actual_parpadeo = pygame.time.get_ticks()
        if tiempo_actual_parpadeo - ultimo_parpadeo > intervalo_parpadeo:
            mensaje_visible = not mensaje_visible
            ultimo_parpadeo = tiempo_actual_parpadeo

        # Lógica de espera
        inicio()
        
        if mensaje_visible:
            screen.blit(mensaje, (width // 2 - mensaje.get_width() // 2, height // 2 + 250))
        
            pygame.display.flip()

    pygame.mixer_music.stop()

def iniciar_new_nivel():
    global current_level, enemy_speed_inicial, enemy_speed, enemys, previous_enemy_speed 
    
    enemys = []
    
    current_level += 1
    previous_enemy_speed = enemy_speed  # Almacena el enemy_speed actual
    enemy_speed = enemy_speed_inicial.get(current_level, previous_enemy_speed)
    print(enemy_speed)
    time.sleep(2)
    reiniciar_cronometro()
       
    if current_level == 2:
        level1_sound.stop()
        nivel_sound.play()
        display_level(f'NIVEL {current_level}')
        reiniciar_cronometro()
        level2_sound.play(-1)
        crear_enemigo(current_level)
    
    if current_level == 3:
        level2_sound.stop()
        nivel_sound.play()
        display_level(f'NIVEL {current_level}')
        reiniciar_cronometro()
        level3_sound.play()
        crear_enemigo(current_level)

    if current_level > max_levels:
        level3_sound.stop()
        finish_sound.play()
        display_finish('''¡Misión cumplida! CONGRATULATIONS, you are still alive.''')
        pygame.quit()
        sys.exit()

def display_message(message):
    text = font_text.render(message, True, red_misil,)
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(6)

def display_level (message1):
    text = font_text1.render(message1, True, (255, 255, 0))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 -85 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(7)
    
def display_finish (message2):
    
    text = font_text2.render(message2, True, (255,255,255))
    screen.blit(text,(width // 2 - text.get_width() // 2, height // 2 -120 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(20)
         
# Función principal del juego
def game():
    global jugador_x, screen, elapsed_time, jugador_y, esperando_inicio, enemys, current_level, enemy_speed, elapsed_time, misiles, reloj, mensaje, mensaje_visible, temporizador_parpadeo, timer_font, elapsed_time, start_time, tecla_espacio_presionada, esperando_inicio, enemys, current_level, enemy_speed, current_time, misiles, misiles_to_remover, enemys_to_remover

    esperando_inicio = True
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Muestra el mensaje al principio del juego
        if esperando_inicio:
            esperar_inicio()
            display_level(f'NIVEL {current_level}')
            reiniciar_cronometro()
            crear_enemigo(current_level)
            esperando_inicio = False
            
            if current_level == 1:
                level1_sound.play(-1)
         
        # Lógica para la entrada del jugador
        entrada_juego()
        disparo()
        mover_enemys()
        mover_misiles()
        clean_display()
        colisiones_balas()
        colisiones_enemigo()
        cronómetro()
        dibujar()

        pygame.time.Clock().tick(60)
        pygame.display.flip()  # Actualizar la pantalla

        if current_level == 1 and remaining_seconds == 0:
            display_message("¡Has perdido!")
            pygame.quit()
            sys.exit()

        if remaining_seconds == -1:
            iniciar_new_nivel()

if __name__ == "__main__":
    game()