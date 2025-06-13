from recursos.basicos import limpar_tela, aguarde
import pygame
import random

pygame.init()

LARGURA, ALTURA = 1000, 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Superman Atira Laser")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

img_fundo = pygame.image.load("assets/fundo.png")
img_fundo = pygame.transform.scale(img_fundo, (LARGURA, ALTURA))

img_superman = pygame.image.load("assets/superman.png")
img_inimigo = pygame.image.load("assets/inimigo.png")
img_laser = pygame.image.load("assets/laser.png")
img_moeda = pygame.image.load("assets/moeda.png")

img_superman = pygame.transform.scale(img_superman, (60, 80))
img_inimigo = pygame.transform.scale(img_inimigo, (120, 80))
img_laser = pygame.transform.scale(img_laser, (7, 32))
img_moeda = pygame.transform.scale(img_moeda, (40, 40))

superman_rect = pygame.Rect(LARGURA // 2 - 5, ALTURA - 100, 60, 80)

velocidade_superman = 9
velocidade_inimigo = 5
velocidade_laser = 15
velocidade_moeda = 5

inimigos = []
lasers = []
moedas = []

pontos = 0
nivel = 1

fonte = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

def gerar_inimigo():
    x = random.randint(100, LARGURA - 120)
    y = random.randint(-800, -150)
    inimigos.append(pygame.Rect(x, y, 120, 80))

def gerar_moeda():
    x = random.randint(50, LARGURA - 90)
    y = random.randint(-700, -100)
    moedas.append(pygame.Rect(x, y, 40, 40))

def desenhar_tudo():
    tela.blit(img_fundo, (0, 0))
    tela.blit(img_superman, superman_rect.topleft)

    for inimigo in inimigos:
        tela.blit(img_inimigo, inimigo.topleft)

    for laser in lasers:
        tela.blit(img_laser, laser.topleft)

    for moeda in moedas:
        tela.blit(img_moeda, moeda.topleft)

    texto_pontos = fonte.render(f"Pontos: {pontos}", True, PRETO)
    texto_nivel = fonte.render(f"Nível: {nivel}", True, PRETO)
    tela.blit(texto_pontos, (20, 20))
    tela.blit(texto_nivel, (20, 60))
    pygame.display.flip()

def colisao(rect1, rect2):
    return rect1.colliderect(rect2)

gerar_inimigo()
gerar_moeda()

rodando = True

while rodando:
    clock.tick(60)
    limpar_tela()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                laser_rect = pygame.Rect(superman_rect.centerx - 3, superman_rect.top - 32, 7, 32)
                lasers.append(laser_rect)

    teclas = pygame.key.get_pressed()
    mov_horizontal = 0
    mov_vertical = 0
    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        mov_horizontal = -velocidade_superman
    elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        mov_horizontal = velocidade_superman

    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        mov_vertical = -velocidade_superman
    elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        mov_vertical = velocidade_superman

    if mov_horizontal != 0 and mov_vertical != 0:
        mov_vertical = 0

    superman_rect.x += mov_horizontal
    superman_rect.y += mov_vertical

    if superman_rect.left < 0:
        superman_rect.left = 0
    if superman_rect.right > LARGURA:
        superman_rect.right = LARGURA
    if superman_rect.top < 0:
        superman_rect.top = 0
    if superman_rect.bottom > ALTURA:
        superman_rect.bottom = ALTURA

    for inimigo in inimigos[:]:
        inimigo.y += velocidade_inimigo
        if inimigo.y > ALTURA:
            inimigos.remove(inimigo)
            gerar_inimigo()
        if colisao(superman_rect, inimigo):
            rodando = False

    for laser in lasers[:]:
        laser.y -= velocidade_laser
        if laser.y < 0:
            lasers.remove(laser)
            continue
        for inimigo in inimigos[:]:
            if colisao(laser, inimigo):
                inimigos.remove(inimigo)
                lasers.remove(laser)
                pontos += 5
                if pontos % 10 == 0:
                    nivel += 1
                    velocidade_inimigo += 0.7
                gerar_inimigo()
                break

    for moeda in moedas[:]:
        moeda.y += velocidade_moeda
        if moeda.y > ALTURA:
            moedas.remove(moeda)
            gerar_moeda()
        if colisao(superman_rect, moeda):
            moedas.remove(moeda)
            pontos += 1
            gerar_moeda()
            if pontos % 10 == 0:
                nivel += 1
                velocidade_inimigo += 0.7
                velocidade_moeda += 0.5

    desenhar_tudo()

limpar_tela()
tela.fill(BRANCO)
fonte_grande = pygame.font.SysFont(None, 80)
texto_game_over = fonte_grande.render("GAME OVER", True, PRETO)
texto_pontos_final = fonte.render(f"Pontuação Final: {pontos}", True, PRETO)
texto_reiniciar = fonte.render("Pressione R para jogar novamente ou ESC para sair", True, PRETO)
tela.blit(texto_game_over, (LARGURA//2 - texto_game_over.get_width()//2, ALTURA//3))
tela.blit(texto_pontos_final, (LARGURA//2 - texto_pontos_final.get_width()//2, ALTURA//2))
tela.blit(texto_reiniciar, (LARGURA//2 - texto_reiniciar.get_width()//2, int(ALTURA//1.5)))
pygame.display.flip()

esperando = True
while esperando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            esperando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                import sys
                import os
                pygame.quit()
                os.execv(sys.executable, ['python'] + sys.argv)
            if evento.key == pygame.K_ESCAPE:
                esperando = False

pygame.quit()
