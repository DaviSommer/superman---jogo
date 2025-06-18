from recursos.basicos import limpar_tela, aguarde
import pygame
import random
from datetime import datetime
import speech_recognition as sr
import pyttsx3

pygame.init()

LARGURA, ALTURA = 1000, 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Superman x Aliens")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (180, 180, 180)

img_fundo = pygame.image.load("assets/fundo.png")
img_fundo = pygame.transform.scale(img_fundo, (LARGURA, ALTURA))

img_superman = pygame.image.load("assets/superman.png")
img_inimigo = pygame.image.load("assets/inimigo.png")
img_laser = pygame.image.load("assets/laser.png")
img_moeda = pygame.image.load("assets/moeda.png")
img_sol = pygame.image.load("assets/sol.png")

img_superman = pygame.transform.scale(img_superman, (60, 80))
img_inimigo = pygame.transform.scale(img_inimigo, (120, 80))
img_laser = pygame.transform.scale(img_laser, (7, 32))
img_moeda = pygame.transform.scale(img_moeda, (40, 40))
som_laser = pygame.mixer.Sound("assets/laser.mp3")
som_dano = pygame.mixer.Sound("assets/dano.mp3")

TAMANHO_SOL_BASE = 70

superman_rect = pygame.Rect(LARGURA // 2 - 5, ALTURA - 100, 60, 80)

velocidade_superman = 14
velocidade_inimigo = 5
velocidade_laser = 15
velocidade_moeda = 5

sol_tamanho_atual = TAMANHO_SOL_BASE
sol_crescendo = True

inimigos = []
lasers = []
moedas = []

pontos = 0
nivel = 1

fonte = pygame.font.SysFont(None, 40)
fonte_grande = pygame.font.SysFont(None, 80)
clock = pygame.time.Clock()

def desenhar_sol_pulsante():
    global sol_tamanho_atual, sol_crescendo, img_sol

    if sol_crescendo:
        sol_tamanho_atual += 0.3
        if sol_tamanho_atual >= TAMANHO_SOL_BASE + 10:
            sol_crescendo = False
    else:
        sol_tamanho_atual -= 0.3
        if sol_tamanho_atual <= TAMANHO_SOL_BASE - 10:
            sol_crescendo = True

    sol_img_redimensionada = pygame.transform.smoothscale(img_sol, (int(sol_tamanho_atual), int(sol_tamanho_atual)))

    pos_x = LARGURA - int(sol_tamanho_atual) - 10
    pos_y = 10

    tela.blit(sol_img_redimensionada, (pos_x, pos_y))

def gerar_inimigo():
    x = random.randint(100, LARGURA - 120)
    y = random.randint(-800, -150)
    inimigos.append(pygame.Rect(x, y, 120, 80))

def gerar_moeda():
    x = random.randint(50, LARGURA - 90)
    y = random.randint(-700, -100)
    moedas.append(pygame.Rect(x, y, 40, 40))

def colisao(rect1, rect2):
    return rect1.colliderect(rect2)

def desenhar_tudo():
    tela.blit(img_fundo, (0, 0))
    tela.blit(img_superman, superman_rect.topleft)
    desenhar_sol_pulsante()

    for inimigo in inimigos:
        tela.blit(img_inimigo, inimigo.topleft)
    for laser in lasers:
        tela.blit(img_laser, laser.topleft)
    for moeda in moedas:
        tela.blit(img_moeda, moeda.topleft)
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, PRETO)
    texto_nivel = fonte.render(f"Nível: {nivel}", True, PRETO)
    texto_pause = fonte.render("Press Space to Pause Game.", True, CINZA)
    tela.blit(texto_pontos, (20, 20))
    tela.blit(texto_nivel, (20, 60))
    tela.blit(texto_pause, (20, 100))
    pygame.display.flip()

def salvar_log(pontos):
    agora = datetime.now()
    data_str = agora.strftime("%d/%m/%Y")
    hora_str = agora.strftime("%H:%M:%S")
    texto_log = f"Pontuação: {pontos} | Data: {data_str} | Hora: {hora_str}\n"
    with open("log_partidas.txt", "a") as arquivo:
        arquivo.write(texto_log)

def ler_ultimas_partidas(qtd=5):
    try:
        with open("log_partidas.txt", "r") as arquivo:
            linhas = arquivo.readlines()
        ultimas = linhas[-qtd:]
        ultimas = [linha.strip() for linha in ultimas]
        return ultimas
    except FileNotFoundError:
        return []

def reconhecer_voz():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    try:
        with mic as source:
            print("Ajustando para ruído ambiente, aguarde...")
            recognizer.adjust_for_ambient_noise(source)
            print("Fale agora seu nickname...")
            audio = recognizer.listen(source, timeout=5)
            print("Reconhecendo...")
        texto = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {texto}")
        return texto
    except sr.WaitTimeoutError:
        print("Tempo esgotado para falar.")
    except sr.UnknownValueError:
        print("Não entendi o que você falou.")
    except sr.RequestError:
        print("Erro na requisição do serviço de reconhecimento.")
    return ""

def tela_inicial():
    entrada = ""
    ativo = True
    fonte_titulo = pygame.font.SysFont(None, 70)
    fonte_texto = pygame.font.SysFont(None, 40)
    while ativo:
        limpar_tela()
        tela.fill(BRANCO)
        titulo = fonte_titulo.render("Superman x Aliens", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 80))
        label = fonte_texto.render("Digite seu nickname (ou pressione V para voz):", True, PRETO)
        tela.blit(label, (LARGURA//2 - label.get_width()//2, 200))

        caixa_texto = pygame.Rect(LARGURA//2 - 150, 250, 300, 40)
        pygame.draw.rect(tela, PRETO, caixa_texto, 2)
        texto_entrada = fonte_texto.render(entrada, True, PRETO)
        tela.blit(texto_entrada, (caixa_texto.x + 5, caixa_texto.y + 5))

        botao_avancar = pygame.Rect(LARGURA//2 - 70, 320, 140, 50)
        pygame.draw.rect(tela, CINZA, botao_avancar)
        texto_botao = fonte_texto.render("Avançar", True, PRETO)
        tela.blit(texto_botao, (botao_avancar.x + (botao_avancar.width - texto_botao.get_width())//2,
                                botao_avancar.y + (botao_avancar.height - texto_botao.get_height())//2))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    entrada = entrada[:-1]
                elif evento.key == pygame.K_RETURN:
                    if entrada.strip():
                        return entrada.strip()
                elif evento.key == pygame.K_v:
                    texto_voz = reconhecer_voz()
                    if texto_voz.strip():
                        entrada = texto_voz.strip()[:15]
                else:
                    if len(entrada) < 15 and evento.unicode.isprintable():
                        entrada += evento.unicode
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_avancar.collidepoint(evento.pos):
                    if entrada.strip():
                        return entrada.strip()

def tela_explicacao(nickname):
    ativo = True
    fonte_titulo = pygame.font.SysFont(None, 60)
    fonte_texto = pygame.font.SysFont(None, 36)
    fonte_botao = pygame.font.SysFont(None, 40)

    texto_desc = [
        f"Bem vindo, {nickname}!",
        "Neste jogo, você controla o Superman.",
        "Use as teclas W, A, S, D ou as setas para se mover.",
        "Clique com o botão esquerdo do mouse para atirar lasers.",
        "Colete moedas para ganhar pontos e evite inimigos.",
        "Aperte ESPAÇO para pausar o jogo.",
        "Boa sorte!"
    ]

    botao_jogar = pygame.Rect(LARGURA//2 - 80, ALTURA - 150, 160, 50)

    while ativo:
        limpar_tela()
        tela.fill(BRANCO)

        titulo = fonte_titulo.render("Como jogar", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 50))

        y_offset = 150
        for linha in texto_desc:
            txt = fonte_texto.render(linha, True, PRETO)
            tela.blit(txt, (LARGURA//2 - txt.get_width()//2, y_offset))
            y_offset += 50

        pygame.draw.rect(tela, CINZA, botao_jogar)
        txt_botao = fonte_botao.render("Jogar", True, PRETO)
        tela.blit(txt_botao, (botao_jogar.x + (botao_jogar.width - txt_botao.get_width())//2,
                              botao_jogar.y + (botao_jogar.height - txt_botao.get_height())//2))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    return

def tela_pause():
    tela.fill(BRANCO)
    fonte_pause = pygame.font.SysFont(None, 100)
    texto_pause = fonte_pause.render("PAUSE", True, PRETO)
    tela.blit(texto_pause, (LARGURA//2 - texto_pause.get_width()//2, ALTURA//2 - texto_pause.get_height()//2))
    pygame.display.flip()

def tela_game_over(pontos, nickname, pular_intro):
    salvar_log(pontos)
    limpar_tela()
    tela.fill(BRANCO)
    agora = datetime.now()
    data_str = agora.strftime("%d/%m/%Y")
    hora_str = agora.strftime("%H:%M:%S")

    texto_game_over = fonte_grande.render("GAME OVER", True, PRETO)
    texto_pontos_final = fonte.render(f"Pontuação Final: {pontos}", True, PRETO)
    texto_data = fonte.render(f"Data: {data_str}", True, PRETO)
    texto_hora = fonte.render(f"Hora: {hora_str}", True, PRETO)
    texto_reiniciar = fonte.render("Pressione R para jogar novamente ou ESC para sair", True, PRETO)

    tela.blit(texto_game_over, (LARGURA//2 - texto_game_over.get_width()//2, ALTURA//8))
    tela.blit(texto_pontos_final, (LARGURA//2 - texto_pontos_final.get_width()//2, ALTURA//8 + 80))
    tela.blit(texto_data, (LARGURA//2 - texto_data.get_width()//2, ALTURA//8 + 130))
    tela.blit(texto_hora, (LARGURA//2 - texto_hora.get_width()//2, ALTURA//8 + 180))

    ultimas_partidas = ler_ultimas_partidas(5)
    y_inicio = ALTURA//2
    titulo_historico = fonte.render("Últimas 5 partidas:", True, PRETO)
    tela.blit(titulo_historico, (LARGURA//2 - titulo_historico.get_width()//2, y_inicio))
    y_inicio += 40

    for partida in ultimas_partidas:
        texto_partida = fonte.render(partida, True, PRETO)
        tela.blit(texto_partida, (LARGURA//2 - texto_partida.get_width()//2, y_inicio))
        y_inicio += 30

    tela.blit(texto_reiniciar, (LARGURA//2 - texto_reiniciar.get_width()//2, int(ALTURA * 0.85)))

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando = False
                    main(nickname=nickname, pular_intro=True)
                if evento.key == pygame.K_ESCAPE:
                    esperando = False
    pygame.quit()
    exit()

def main(nickname=None, pular_intro=False):
    global pontos, nivel, velocidade_inimigo, velocidade_moeda, superman_rect, lasers, inimigos, moedas, sol_tamanho_atual, sol_crescendo

    if not nickname:
        nickname = tela_inicial()
    if not pular_intro:
        tela_explicacao(nickname)

    pontos = 0
    nivel = 1
    velocidade_inimigo = 5
    velocidade_moeda = 5
    lasers = []
    inimigos = []
    moedas = []
    superman_rect = pygame.Rect(LARGURA // 2 - 5, ALTURA - 100, 60, 80)

    sol_tamanho_atual = TAMANHO_SOL_BASE
    sol_crescendo = True

    gerar_inimigo()
    gerar_moeda()

    rodando = True
    pausado = False

    while rodando:
        clock.tick(60)
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

        limpar_tela()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN and not pausado:
                if evento.button == 1:
                    laser_rect = pygame.Rect(superman_rect.centerx - 3, superman_rect.top - 32, 7, 32)
                    lasers.append(laser_rect)
                    som_laser.play()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                    if pausado:
                        tela_pause()

        if not pausado:
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
                    som_dano.play()
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

    tela_game_over(pontos, nickname, pular_intro)

if __name__ == "__main__":
    main()
