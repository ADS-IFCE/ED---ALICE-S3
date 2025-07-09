#config iniciais
import pygame
import random

pygame.init()
pygame.display.set_caption("Jogo Snake")
largura, altura = 1000, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

#cores RGB
azul = (178,218,250)
azulnavy = (0, 0, 86)
azulmar = (41, 99, 147)
branca = (255, 255, 255)

#parametros da cobrinha
tamanhoDoQuadrado = 20
velocidadeAtt = 10

#usa o modo random pra gerar dois valores aleatorios de x e y
def gerar_comida():
    #usei -tamanhoDoQuadrado para não correr risco da comida gerar no último pixel do quadrado e ficar para fora
    #para garantir que a comida esteja sempre na mesma reta que a cobrinha, dividimos pelo tamanho do quadrado
    #pode ser que dê num decimal, então é melhor arredondar
    #multiplica por 10 de novo para ter uma verificação
    comida_x = round(random.randrange(0,largura - tamanhoDoQuadrado) / 20.0) * 20
    comida_y = round(random.randrange(0,altura - tamanhoDoQuadrado) / 20.0) * 20
    return comida_x, comida_y
def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, azulmar, (comida_x, comida_y, tamanho, tamanho))

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, azulnavy, (pixel[0], pixel[1], tamanho, tamanho))

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont('sans-serif', 40)
    texto = fonte.render(f"Pontos: {pontuacao}", True, branca) #True é só para arrendondar a fonte, brincadeira visual
    tela.blit(texto, [1, 1])

def selecionar_velocidade(tecla):
    if tecla == pygame.K_DOWN:
        velocidade_x = 0
        velocidade_y = tamanhoDoQuadrado
    elif tecla == pygame.K_UP:
        velocidade_x = 0
        velocidade_y = - tamanhoDoQuadrado
    elif tecla == pygame.K_RIGHT:
        velocidade_x = tamanhoDoQuadrado
        velocidade_y = 0
    elif tecla == pygame.K_LEFT:
        velocidade_x = - tamanhoDoQuadrado
        velocidade_y = 0

    return velocidade_x, velocidade_y

def rodar_jogo():
    fim_jogo = False

    x = largura /2
    y = altura /2

    velocidade_x = 0
    velocidade_y = 0

    tamanhoCobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill(azul)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fim_jogo = True
            elif event.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(event.key)


        #desenhar_comida
        desenhar_comida(tamanhoDoQuadrado, comida_x, comida_y)

        #atualizar posição da cobrinha
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True
        x += velocidade_x
        y += velocidade_y

        #desenhar_cobra
        pixels.append([x, y])
        if len(pixels) > tamanhoCobra:
            del pixels[0]

        #caso a cobrinha bata nela mesma
        #coloca o -1 para não fechar o jogo logo de início, porque vai apagar o que adicionamos antes
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fim_jogo = True
        desenhar_cobra(tamanhoDoQuadrado, pixels)

        #desenhar_pontos
        desenhar_pontuacao(tamanhoCobra - 1)

        #atualização da tela
        pygame.display.update()

        #criar uma nova comida
        if x == comida_x and y == comida_y:
            tamanhoCobra += 1
            comida_x, comida_y = gerar_comida()
        relogio.tick(velocidadeAtt)

rodar_jogo()
