import pygame
import os
pygame.font.init()
pygame.mixer.init()

#ventana o display 
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naves espaciales")

#constantes para funciones
#colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
#fuentes de texto
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 90)
#sonido
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))
#Velocidad, tamaños
FPS = 60
VEL = 5
#bullets
MAX_BULLETS = 3
BULLETS_VEL = 7
BULLET_WIDTH = 15
BULLET_HEIGHT = 8
#rockets
MAX_ROCKETS = 5
ROCKETS_VEL = 15
ROCKET_WIDTH = 25
ROCKET_HEIGHT = 18

SPACESHIP_WIDTH = 45
SPACESHIP_HEIGHT = 40
BORDER = pygame.Rect(WIDTH//2 - 3, 0, 6, HEIGHT)

#nuevos eventos para saber cuando el objeto es golpeado
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
YELLOW_HIT_2 = pygame.USEREVENT + 3
RED_HIT_2 = pygame.USEREVENT + 4

#imágenes de personajes y fondo
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'nave_amarilla.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'nave_roja.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.jpg')), (WIDTH, HEIGHT))

BALA_ROJA_IMAGE = pygame.image.load(os.path.join('Assets', 'bala_roja.png'))
BALA_ROJA = pygame.transform.scale(BALA_ROJA_IMAGE, (BULLET_WIDTH, BULLET_HEIGHT))
BALA_AMARILLA_IMAGE = pygame.image.load(os.path.join('Assets', 'bala_amarilla.png'))
BALA_AMARILLA = pygame.transform.scale(BALA_AMARILLA_IMAGE, (BULLET_WIDTH, BULLET_HEIGHT))

MISIL_ROJO_IMAGE = pygame.image.load(os.path.join('Assets', 'rocket_red.png'))
MISIL_ROJO = pygame.transform.scale(MISIL_ROJO_IMAGE, (ROCKET_WIDTH, ROCKET_HEIGHT))
MISIL_AMARILLO_IMAGE = pygame.image.load(os.path.join('Assets', 'rocket_yellow.png'))
MISIL_AMARILLO = pygame.transform.scale(MISIL_AMARILLO_IMAGE, (ROCKET_WIDTH, ROCKET_HEIGHT))

#función para mostrar los gráficos
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_rockets, yellow_rockets):
    WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))

    red_health_text = HEALTH_FONT.render('Vida: ' + str(red_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    yellow_health_text = HEALTH_FONT.render('Vida: ' + str(yellow_health), 1, WHITE)
    WIN.blit(yellow_health_text, ( 10, 10))

    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in red_bullets:
        WIN.blit(BALA_ROJA, bullet)

    for bullet in yellow_bullets:
        WIN.blit(BALA_AMARILLA, bullet)
        
    for rocket in red_rockets:
        WIN.blit(MISIL_ROJO, rocket)

    for rocket in yellow_rockets:
        WIN.blit(MISIL_AMARILLO, rocket)

    pygame.display.update()

#función para configurar los controles
def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #IZQUIERDA
            yellow.x -= VEL
        if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #DERECHA
            yellow.x += VEL
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #ARRIBA
            yellow.y -= VEL
        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #ABAJO
            yellow.y += VEL

def red_handle_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #IZQUIERDA
            red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH : #DERECHA
            red.x += VEL
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #ARRIBA
            red.y -= VEL
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: #ABAJO
            red.y += VEL

#función para el movimiento de las balas
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def handle_rockets(yellow_rockets, red_rockets, yellow, red):
    for rocket in yellow_rockets:
        rocket.x += ROCKETS_VEL
        if red.colliderect(rocket):
            pygame.event.post(pygame.event.Event(RED_HIT_2))
            yellow_rockets.remove(rocket)
    
    for rocket in red_rockets:
        rocket.x -= ROCKETS_VEL
        if yellow.colliderect(rocket):
            pygame.event.post(pygame.event.Event(YELLOW_HIT_2))
            red_rockets.remove(rocket)
    
# función para escribir el texto cuando alguien gana
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(4000)


#función principal de ejecución del juego
def main():
    #jugadores
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)    
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  

    #lista que aloja balas, si tiene mas de 4 entonces no dispara
    red_bullets = []
    red_rockets = []
    yellow_bullets = []
    yellow_rockets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run: #loop infinito que ejecuta el juego
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN: #disparar armas
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                #MISILES!! rockets
                if event.key == pygame.K_LSHIFT and len(yellow_rockets) < MAX_ROCKETS:
                    rocket = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, ROCKET_WIDTH, ROCKET_HEIGHT)
                    yellow_rockets.append(rocket)
                    BULLET_FIRE_SOUND.play() #cambiar sonidos
                
                if event.key == pygame.K_RSHIFT and len(red_rockets) < MAX_ROCKETS:
                    rocket = pygame.Rect(red.x, red.y + red.height//2 - 2, ROCKET_WIDTH, ROCKET_HEIGHT)
                    red_rockets.append(rocket)
                    BULLET_FIRE_SOUND.play()    
                

            if event.type == RED_HIT: # restar vida por balas
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
                
            if event.type == RED_HIT_2: # restar vida por misiles
                red_health -= 2
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT_2:
                yellow_health -= 2
                BULLET_HIT_SOUND.play()

        #texto de ganador
        winner_text = ""
        if red_health <= 0:
            winner_text = "Amarillo Gana!"
        
        if yellow_health <= 0:
            winner_text = "Rojo Gana!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()      
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_rockets, yellow_rockets)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        handle_rockets(yellow_rockets, red_rockets, yellow, red)

    main() #reiniciar juego al ganar

if __name__ == "__main__": #archivo principal
    main()
