#bibliotecas
import pygame 
import math #para o calculo da distância entre coordenadas
import random #para a posição do inimigo
from pygame import FULLSCREEN, RESIZABLE, mixer #para adicionar músicas ao jogo

#inicializando o pygame
pygame.init()

#criando uma tela
screen = pygame.display.set_mode((800, 600))

#inserindo título da janela
pygame.display.set_caption("Invasores do Espaço")

#background
background = pygame.image.load('background.png')

#musica de fundo
mixer.music.load('background.mp3')
mixer.music.play(-1)

#inserindo icone
icone = pygame.image.load('ufo.png')
pygame.display.set_icon(icone)

#posição do jogador
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
#variavel para mudar a posição do jogador
playerX_change = 0

#criando multiplos inimigos
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemys = 6

#posição do inimigo
for i in range(num_of_enemys):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    #variavel para mudar a posição do inimigo
    enemyX_change.append(4)
    enemyY_change.append(40)

#posição do tiro
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
#variavel para mudar a posição do tiro
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#pontuação
score_valor = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

#fim de jogo
game_over = False

#fonte texto de fim de jogo
font_over = pygame.font.Font("freesansbold.ttf", 64)

#função para mostrar a pontuação
def mostrar_pontuacao(x, y):
    score = font.render("Pontuação: %s" %score_valor, True, (255, 255, 255))
    screen.blit(score, (x, y))

#função de fim de jogo
def game_over_text():
    if game_over == True:
        over_score = font_over.render("FIM DE JOGO", True, (255, 255, 255))
        screen.blit(over_score, (200, 250))    
        mostrar_pontuacao(textX, textY)
        pygame.display.update()

#função para desenhar o player
def player(x, y):
    screen.blit(playerImg, (x, y))

#função para desenhar o inimigo
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

#função para desenhar o tiro
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

#função para a colisão entre o tiro e o inimigo
def isCollision(enemyX, enemyY, bulletX, bulletY):
    collision = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if collision < 27:
        return True
    else:
        return False

#função para a colisão entre o player e o inimigo
def isDeath(enemyX, enemyY, playerX, playerY):
    death = math.sqrt((math.pow(enemyX-playerX, 2)) + (math.pow(enemyY-playerY, 2)))
    if death <= 27:
        return True
    else:
        return False

#principal loop do jogo
running = True
while running:
    # RGB - red, green, blue (cor da janela)
    screen.fill((0, 0, 0))
    #imagem background
    screen.blit(background, (0, 0)) 
    #comando para encerrar o loop 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #checar se uma tecla é pressionada (colocar os inputs do teclado)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -5
        if event.key == pygame.K_RIGHT:
            playerX_change = 5 
        if event.key == pygame.K_UP:
            if bullet_state == "ready":
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                #dar a coordenada atual x da nave 
                bulletX = playerX
                fire_bullet(bulletX, bulletY) 

    #parar o objeto quando nenhuma tecla for pressionada
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
             playerX_change = 0

    #codição para mexer o player para esquerda e direita
    playerX += playerX_change

    #condição para impedir que o player saia da tela
    if playerX <= 0:
        playerX = 0

    elif playerX >= 736:
        playerX = 736

    #movimentação do inimigo(s)  
    for i in range(num_of_enemys):

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
        #velocidade do inimigo
            enemyX_change[i] = 6
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
        #velocidade do inimigo
            enemyX_change[i] = -6
            enemyY[i] += enemyY_change[i]

        #colissão entre tiro e inimigo
        colissão = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if colissão:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            #aumenta a pontuação em 1 toda vez que um inimigo é atingido
            score_valor += 1
            #respaw do inimigo toda vez que um for acertado
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        
        #colissão entre player e inimigo (fim de jogo)
        game_over = isDeath(enemyX[i], enemyY[i], playerX, playerY)
        if game_over == True:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            game_over_text()
            score_valor = 0
            #loop para manter a tela de gameover
            done = False
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        done = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            done = True
                            #resetar a posição do player
                            playerX = 370
                            playerY = 480
                            #resetar a posição dos inimigos
                            enemyImg = []
                            enemyX = []
                            enemyY = []
                            enemyX_change = []
                            enemyY_change = []
                            num_of_enemys = 6
                            for i in range(num_of_enemys):
                                enemyImg.append(pygame.image.load('enemy.png'))
                                enemyX.append(random.randint(0, 736))
                                enemyY.append(random.randint(50, 150))
                                #variavel para mudar a posição do inimigo
                                enemyX_change.append(4)
                                enemyY_change.append(40)
                    pygame.display.update()
    
        enemy(enemyX[i], enemyY[i], i)
    
    #movimentação do tiro
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    mostrar_pontuacao(textX, textY)
    pygame.display.update()

