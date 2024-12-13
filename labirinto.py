import pygame as pg
import sys
from gerar_labirinto import *
from PIL import Image
from random import choice

# Configurações iniciais
tamanho = [15, 10]  # Número de linhas e colunas do labirinto
size = 33  # Tamanho do espaço entre as linhas e colunas

# Retorna uma lista com duas sublistas contendo 1 para parede e 0 para espaço vazio
l = gerar_labirinto(tamanho[0], tamanho[1])

# Cria uma imagem em branco para o labirinto
img_new = Image.new('RGB', (tamanho[0]*(size+1)+1, tamanho[1]*(size+1)+1), (0, 0, 0))
draw = ImageDraw.Draw(img_new)

# Desenha o labirinto na "máscara"
desenhar_labirinto_pillow(draw, tamanho, l, size)

# Salva a imagem com o labirinto desenhado
img_new.save("fundo_verde.png")

size += 1
id_jogador = 0

pg.init()
pg.font.init()
font = pg.font.Font(None, 36)

pg.mouse.set_visible(False)
tela = pg.display.set_mode((tamanho[0]*size+1, tamanho[1]*size+1))
fps = pg.time.Clock()
fundo = pg.image.load("fundo_verde.png")
fundo_rect = fundo.get_rect()
img = Image.open("fundo_verde.png")
img = img.convert('RGB')
rgb = img.load()

# Carregar a imagem do personagem
personagem_img = pg.image.load("personagem.png")
personagem_img = pg.transform.scale(personagem_img, (size - 2, size - 2))  # Ajusta o tamanho do personagem

posicoes = {id_jogador: [[tamanho[0]*size-size/2, size/2]]}
pg.mouse.set_pos(posicoes[id_jogador][0])
x_mouse, y_mouse = posicoes[id_jogador][0]
tela.blit(fundo, fundo_rect)
pg.display.update()

# Função para gerar posições das letras sem sobreposição
def gerar_posicoes_letras(tamanho, size, letras):
    posicoes = []
    for letra in letras:
        while True:
            # Gera uma nova posição aleatória
            x = randint(1, tamanho[0] - 2) * size + size // 2
            y = randint(1, tamanho[1] - 2) * size + size // 2
            nova_posicao = (x, y)
            
            # Verifica se a nova posição é suficientemente distante das posições existentes
            if all(
                abs(nova_posicao[0] - pos[0]) >= size and abs(nova_posicao[1] - pos[1]) >= size
                for pos in posicoes
            ):
                posicoes.append(nova_posicao)
                break
    return posicoes

# Lista de palavras e escolha aleatória
lista_palavras = ["PYTHON", "LABIRINTO", "JOGO", "DESAFIO"]
palavra_secreta = choice(lista_palavras)
letras_palavra = list(palavra_secreta)
letras_coletadas = []
posicoes_letras = gerar_posicoes_letras(tamanho, size, letras_palavra)

# Variáveis de jogabilidade
angulo_personagem = 0
escala_atual = 1.0
distorcao_horizontal = True
refletir_automatico = False

# Vincular letras às suas posições
letras_posicionadas = list(zip(letras_palavra, posicoes_letras))

# Função para soltar a última letra coletada
def soltar_ultima_letra(letras_coletadas, letras_posicionadas, posicoes_letras, tamanho, size):
    if letras_coletadas:
        letra, _ = letras_coletadas.pop()  # Remove a última letra coletada

        while True:
            # Gera uma nova posição aleatória para a letra
            x = randint(1, tamanho[0] - 2) * size + size // 2
            y = randint(1, tamanho[1] - 2) * size + size // 2
            nova_posicao = (x, y)

            # Garante que a nova posição não conflita com as posições existentes
            if nova_posicao not in posicoes_letras and all(
                abs(nova_posicao[0] - pos[0]) >= size and abs(nova_posicao[1] - pos[1]) >= size
                for _, pos in letras_posicionadas
            ):
                posicoes_letras.append(nova_posicao)
                letras_posicionadas.append((letra, nova_posicao))  # Reposiciona a letra
                break

# Função para desenhar as letras na tela
def desenhar_letras(tela, letras_posicionadas, letras_coletadas):
    for letra, pos in letras_posicionadas:
        # Define a cor dependendo se a letra já foi coletada
        cor = (100, 100, 100) if (letra, pos) in letras_coletadas else (255, 255, 255)
        letra_surface = font.render(letra, True, cor)
        letra_rect = letra_surface.get_rect(center=(pos[0], pos[1]))
        tela.blit(letra_surface, letra_rect.topleft)

# Função para verificar coleta de letras
def verificar_coleta_letra(posicao_jogador, letras_posicionadas, letras_coletadas, size, coletar):
    for letra, pos in letras_posicionadas:
        if abs(posicao_jogador[0] - pos[0]) < size // 2 and abs(posicao_jogador[1] - pos[1]) < size // 2:
            # Coleta a letra apenas se a tecla espaço for pressionada e ela ainda não foi coletada
            if coletar and (letra, pos) not in letras_coletadas:
                letras_coletadas.append((letra, pos))
                print(f"Coletada: {letra}")
    return letras_coletadas

# Função para verificar vitória
def verificar_vitoria(posicao, tamanho, size, letras_coletadas, palavra_secreta):
    jogador_x, jogador_y = posicao
    final_x, final_y = size // 2, tamanho[1] * size - size // 2
    palavra_coletada = "".join(letra for letra, _ in letras_coletadas)
    if jogador_x == final_x and jogador_y == final_y and palavra_coletada == palavra_secreta:
        return True
    return False

coletar_letra = False
vencedor = False

while True:
    fps.tick(10)
    tela.blit(fundo, fundo_rect)

    for event in pg.event.get():
        x_mouse, y_mouse = pg.mouse.get_pos()
        jogou = False

        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:  # Coletar letra
                coletar_letra = True
            elif event.key == pg.K_s:  # Soltar última letra
                soltar_ultima_letra(letras_coletadas, letras_posicionadas, posicoes_letras, tamanho, size)
            elif event.key == pg.K_LEFT:  # Movimentar para a esquerda
                posicoes, jogou = move.esquerda(rgb, size, posicoes, id_jogador)
                angulo_personagem = 180
            elif event.key == pg.K_RIGHT:  # Movimentar para a direita
                posicoes, jogou = move.direita(rgb, size, posicoes, id_jogador)
                angulo_personagem = 0
            elif event.key == pg.K_UP:  # Movimentar para cima
                posicoes, jogou = move.cima(rgb, size, posicoes, id_jogador)
                angulo_personagem = 90
            elif event.key == pg.K_DOWN:  # Movimentar para baixo
                posicoes, jogou = move.baixo(rgb, size, posicoes, id_jogador)
                angulo_personagem = 270

        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                coletar_letra = False

    # Verifica se o jogador coleta uma letra
    letras_coletadas = verificar_coleta_letra(
        posicoes[id_jogador][0], letras_posicionadas, letras_coletadas, size, coletar_letra
    )

    # Verifica vitória ao chegar no quadrado final e ter a palavra completa
    if verificar_vitoria(posicoes[id_jogador][0], tamanho, size, letras_coletadas, palavra_secreta):
        vencedor = True

    if vencedor:
        print("Você venceu o jogo! Parabéns!")
        tela.fill((0, 0, 0))
        texto_vitoria = font.render("Você venceu! Parabéns!", True, (128, 0, 128))  # Cor roxa
        tela.blit(texto_vitoria, (tamanho[0] * size // 4, tamanho[1] * size // 2))
        pg.display.update()
        pg.time.wait(3000)
        break

    # Desenha as letras no labirinto
    desenhar_letras(tela, letras_posicionadas, letras_coletadas)

    # Exibe o personagem na posição atual com rotação
    personagem_rotacionado = pg.transform.rotate(personagem_img, angulo_personagem)
    personagem_rect = personagem_rotacionado.get_rect(center=posicoes[id_jogador][0])
    tela.blit(personagem_rotacionado, personagem_rect.topleft)

    # Exibe as letras coletadas
    palavra_atual = "".join(letra for letra, _ in letras_coletadas)
    texto_coletadas = font.render("Coletadas: " + palavra_atual, True, (255, 255, 255))
    tela.blit(texto_coletadas, (10, 10))

    # Exibe a palavra completa
    texto_palavra = font.render("Palavra: " + palavra_secreta, True, (255, 255, 255))
    tela.blit(texto_palavra, (10, 40))

    pg.display.update()
