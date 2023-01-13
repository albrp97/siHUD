import os
import time

import pygame

pygame.init()

negro = pygame.Color("#2E3440")
gris = pygame.Color("#4C566A")
grisclaro = pygame.Color("#D8DEE9")
blanco = pygame.Color("#ECEFF4")
rojo = pygame.Color("#BF616A")
rojoclaro = pygame.Color("#afa4ee")
naranja = pygame.Color("#D08770")
amarillo = pygame.Color("#EBCB8B")
verde = pygame.Color("#A3BE8C")
violeta = pygame.Color("#B48EAD")
violetaclaro = pygame.Color("#afa4ee")
azul = pygame.Color("#5E81AC")
cyan = pygame.Color("#88C0D0")

# todo get exact half
os.environ['SDL_VIDEO_WINDOW_POS'] = "2000,100"
screen = pygame.display.set_mode((1000, 450))
pygame.display.set_caption("HANKA TERMINAL")

screen.fill(negro)
pygame.display.update()

running = True


def pintarTitulo():
    screen.fill(negro)

    font = "./files/mplus-1mn-bold.ttf"
    myfont = pygame.font.Font(font, 25)
    label = myfont.render("人    I    知    能    や    ボ    ロ    ツ    ト    エ    学", True, blanco)
    screen.blit(label, (120, 30))



    font = "./files/JetBrainsMono-Regular.ttf"
    myfont = pygame.font.Font(font, 20)
    mainTitleColor=cyan
    i = 75
    aumento = 25

    # todo make gradient

    label = myfont.render("#####    #####       #####     #####       ##### #####    ######      #####", True, mainTitleColor)
    screen.blit(label, (10, i))
    i+=aumento
    label = myfont.render("#####    #####      #######    ######      ##### #####   ######      #######", True, mainTitleColor)
    screen.blit(label, (10, i))
    i += aumento
    label = myfont.render("#####    #####     #########   #######     ##### ##### ######       #########", True, mainTitleColor)
    screen.blit(label, (10, i))
    i += aumento
    label = myfont.render("##############    ##### #####  ########    ##### ##########        ##### #####", True, mainTitleColor)
    screen.blit(label, (10, i))
    i += aumento
    label = myfont.render("##############   #####   ##### ##########  ##### ###########      #####   #####", True, mainTitleColor)
    screen.blit(label, (10, i))
    i += aumento
    label = myfont.render("#####    #####  #####     ########## ##### ##### ###### ######   #####     #####", True, mainTitleColor)
    screen.blit(label, (10, i))
    i += aumento
    label = myfont.render("#####    ##### #####       #########  ########## #####   ###### #####       #####", True, mainTitleColor)
    screen.blit(label, (10, i))
    i += aumento
    label = myfont.render("#####    ##########         ########   ######### #####    ##########         #####", True, mainTitleColor)
    screen.blit(label, (10, i))
    i += aumento

    # font = "./files/mplus-1mn-bold.ttf"
    myfont = pygame.font.Font(font, 28)
    label = myfont.render("R     O     B     O     T     I     C     S", True, blanco)
    screen.blit(label, (150, 280))


    pygame.display.update()


entrada = ""
entradaFantasma=""
palabrasClave=["exit","track","gameNews"]
once=False
while running:

    for event in pygame.event.get():
        if not once:
            pintarTitulo()
            font = "./files/JetBrainsMono-Regular.ttf"
            myfont = pygame.font.Font(font, 20)
            label = myfont.render(">", True, blanco)
            screen.blit(label, (10, 400))
            label = myfont.render("|", True, grisclaro)
            screen.blit(label, (30, 400))
            pygame.display.update()
            once = True
        if event.type == pygame.KEYDOWN:
            # print(pygame.key.name(event.key))
            font = "./files/JetBrainsMono-Regular.ttf"
            myfont = pygame.font.Font(font, 20)
            pygame.draw.rect(screen, negro, pygame.Rect(30, 400, 500, 30))
            if len(pygame.key.name(event.key)) == 1:
                entrada += pygame.key.name(event.key)
            elif pygame.key.name(event.key) == "backspace":
                entrada = entrada[:-1]
            elif pygame.key.name(event.key) == "space":
                entrada += " "
            elif pygame.key.name(event.key) == "return":
                # todo ejecutar
                print(entrada)
                if entrada=="exit":
                    running = False
            elif pygame.key.name(event.key) == "escape":
                entrada = ""

            colorClave=blanco
            if len(entrada)>0:
                for clave in palabrasClave:
                    entradaFantasma = ""
                    # todo make most used commands counter
                    if len(entrada)<=len(clave) and entrada==clave[0:len(entrada)]:
                        colorClave=azul
                        for i in range(len(entrada)):
                            entradaFantasma+=" "
                        entradaFantasma+=clave[len(entrada):]
                        break
                if pygame.key.name(event.key) == "tab":
                    entrada = clave
                    entradaFantasma=""
            else:
                entradaFantasma = ""

            label = myfont.render(">", True, blanco)
            screen.blit(label, (10, 400))
            label = myfont.render(entrada, True, colorClave)
            screen.blit(label, (30, 400))
            label = myfont.render(entradaFantasma, True, gris)
            screen.blit(label, (30, 400))
            label=myfont.render("|", True, grisclaro)
            screen.blit(label, (25+12*len(entrada), 400))
            pygame.display.update()

        elif event.type == pygame.QUIT:
            running = False
