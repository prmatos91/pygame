import pygame as pg
import sys
from gerar_labirinto import *
from PIL import Image
from random import choice, randint

tamanho = [15, 10] 
size = 33 

l = gerar_labirinto(tamanho[0], tamanho[1])

img_new = Image.new('RGB', (tamanho[0] * (size + 1) + 1, tamanho[1] * (size + 1) + 1), (0, 0, 0))
draw = ImageDraw.Draw(img_new)

desenhar_labirinto_pillow(draw, tamanho, l, size)

img_new.save("fundo_verde.png")

size += 1
id_jogador = 0

pg.init()
pg.font.init()
font = pg.font.Font(None, 36)

pg.mouse.set_visible(False)
tela = pg.display.set_mode((tamanho[0] * size + 1, tamanho[1] * size + 1))
fps = pg.time.Clock()
fundo = pg.image.load("fundo_verde.png")
fundo_rect = fundo.get_rect()
img = Image.open("fundo_verde.png")
img = img.convert('RGB')
rgb = img.load()

personagem_img = pg.image.load("personagem.png")
personagem_img = pg.transform.scale(personagem_img, (size - 2, size - 2)) 

posicoes = {id_jogador: [[tamanho[0] * size - size / 2, size / 2]]}
pg.mouse.set_pos(posicoes[id_jogador][0])
x_mouse, y_mouse = posicoes[id_jogador][0]
tela.blit(fundo, fundo_rect)
pg.display.update()

def gerar_posicoes_letras(tamanho, size, letras):
    posicoes = []
    for letra in letras:
        while True:
            x = randint(1, tamanho[0] - 2) * size + size // 2
            y = randint(1, tamanho[1] - 2) * size + size // 2
            nova_posicao = (x, y)
            if all(
                abs(nova_posicao[0] - pos[0]) >= size and abs(nova_posicao[1] - pos[1]) >= size
                for pos in posicoes
            ):
                posicoes.append(nova_posicao)
                break
    return posicoes

lista_palavras = ["PYTHON", "LABIRINTO", "JOGO", "DESAFIO"]
palavra_secreta = choice(lista_palavras)
letras_palavra = list(palavra_secreta)
letras_coletadas = []
posicoes_letras = gerar_posicoes_letras(tamanho, size, letras_palavra)

angulo_personagem = 0

letras_posicionadas = list(zip(letras_palavra, posicoes_letras))

def soltar_ultima_letra(letras_coletadas, letras_posicionadas, posicoes_letras, tamanho, size):
    if letras_coletadas:
        letra, _ = letras_coletadas.pop()
        tentativas = 0
        max_tentativas = 100  

        while tentativas < max_tentativas:
            x = randint(1, tamanho[0] - 2) * size + size // 2
            y = randint(1, tamanho[1] - 2) * size + size // 2
            nova_posicao = (x, y)

            if nova_posicao not in posicoes_letras and all(
                abs(nova_posicao[0] - pos[0]) >= size and abs(nova_posicao[1] - pos[1]) >= size
                for _, pos in letras_posicionadas
            ):
                posicoes_letras.append(nova_posicao)
                letras_posicionadas.append((letra, nova_posicao))
                return
            tentativas += 1

        print("Não foi possível encontrar uma posição válida; soltando próximo ao jogador.")
        jogador_x, jogador_y = posicoes[id_jogador][0]
        nova_posicao = (jogador_x + size, jogador_y + size)
        posicoes_letras.append(nova_posicao)
        letras_posicionadas.append((letra, nova_posicao))

def desenhar_letras(tela, letras_posicionadas, letras_coletadas):
    for letra, pos in letras_posicionadas:
        cor = (100, 100, 100) if (letra, pos) in letras_coletadas else (255, 255, 255)
        letra_surface = font.render(letra, True, cor)
        letra_rect = letra_surface.get_rect(center=(pos[0], pos[1]))
        tela.blit(letra_surface, letra_rect.topleft)

def verificar_coleta_letra(posicao_jogador, letras_posicionadas, letras_coletadas, size, coletar):
    for letra, pos in letras_posicionadas:
        if abs(posicao_jogador[0] - pos[0]) < size // 2 and abs(posicao_jogador[1] - pos[1]) < size // 2:
            if coletar and (letra, pos) not in letras_coletadas:
                letras_coletadas.append((letra, pos))
                print(f"Coletada: {letra}")
    return letras_coletadas

def verificar_vitoria(posicao, tamanho, size, letras_coletadas, palavra_secreta):
    jogador_x, jogador_y = posicao
    final_x, final_y = size // 2, tamanho[1] * size - size // 2
    palavra_coletada = "".join(letra for letra, _ in letras_coletadas)
    return jogador_x == final_x and jogador_y == final_y and palavra_coletada == palavra_secreta

coletar_letra = False
vencedor = False

while True:
    fps.tick(10)
    tela.blit(fundo, fundo_rect)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                coletar_letra = True
            elif event.key == pg.K_s:
                soltar_ultima_letra(letras_coletadas, letras_posicionadas, posicoes_letras, tamanho, size)
            elif event.key == pg.K_LEFT:
                posicoes, _ = move.esquerda(rgb, size, posicoes, id_jogador)
                angulo_personagem = 180
            elif event.key == pg.K_RIGHT:
                posicoes, _ = move.direita(rgb, size, posicoes, id_jogador)
                angulo_personagem = 0
            elif event.key == pg.K_UP:
                posicoes, _ = move.cima(rgb, size, posicoes, id_jogador)
                angulo_personagem = 90
            elif event.key == pg.K_DOWN:
                posicoes, _ = move.baixo(rgb, size, posicoes, id_jogador)
                angulo_personagem = 270

        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                coletar_letra = False

    letras_coletadas = verificar_coleta_letra(
        posicoes[id_jogador][0], letras_posicionadas, letras_coletadas, size, coletar_letra
    )

    if verificar_vitoria(posicoes[id_jogador][0], tamanho, size, letras_coletadas, palavra_secreta):
        vencedor = True

    if vencedor:
        print("Você venceu o jogo! Parabéns!")
        tela.fill((0, 0, 0))
        texto_vitoria = font.render("Você venceu! Parabéns!", True, (128, 0, 128))
        tela.blit(texto_vitoria, (tamanho[0] * size // 4, tamanho[1] * size // 2))
        pg.display.update()
        pg.time.wait(3000)
        break

    desenhar_letras(tela, letras_posicionadas, letras_coletadas)

    personagem_rotacionado = pg.transform.rotate(personagem_img, angulo_personagem)
    personagem_rect = personagem_rotacionado.get_rect(center=posicoes[id_jogador][0])
    tela.blit(personagem_rotacionado, personagem_rect.topleft)

    palavra_atual = "".join(letra for letra, _ in letras_coletadas)
    texto_coletadas = font.render("Coletadas: " + palavra_atual, True, (255, 255, 255))
    tela.blit(texto_coletadas, (10, 10))

    texto_palavra = font.render("Palavra: " + palavra_secreta, True, (255, 255, 255))
    tela.blit(texto_palavra, (10, 40))

    pg.display.update()
