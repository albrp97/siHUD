import os
import time
import json
import pygame
import json
import os
import datetime

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

# todo get exact coordinate
os.environ['SDL_VIDEO_WINDOW_POS'] = "3000,1000"
screen = pygame.display.set_mode((600, 720))
pygame.display.set_caption("TRACK")

screen.fill(negro)
pygame.display.update()

current_time = datetime.datetime.now()
currentAnio = current_time.year
currentMes = current_time.month

mes=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def createDict(anio=currentAnio, mes=currentMes):
    targetDict = {
        "anio": anio,
        "mes": mes,

        "income": 0,
        "histIncome": [],

        "extras": 0,
        "histExtras": [],

        "vivir": 0,
        "ratioVivir": .5,
        "histVivir": [],
        "expectedVivir": 0,
        "remainingVivir": 0,

        "gastar": 0,
        "ratioGastar": .3,
        "histGastar": [],
        "expectedGastar": 0,
        "acomulatedGastar": 0,
        "remainingGastar": 0,

        "save": 0,
        "ratioSave": .2,
        "expectedSave": 0,
        "extraSaves": [],

        "offsetGastar": 0,
        "offsetSave": 0
    }
    return targetDict

def calculateVariables(originDict):
    # total incomes
    originDict["income"] = sum(originDict["histIncome"])
    # total extras
    originDict["extras"] = sum(originDict["histExtras"])

    # spent on vivir
    originDict["vivir"] = sum(originDict["histVivir"])
    # expected vivir this month
    originDict["expectedVivir"] = originDict["income"] * originDict["ratioVivir"]
    # remaining gastar this month
    originDict["remainingVivir"] = originDict["expectedVivir"] - originDict["vivir"]

    # spent on gastar
    originDict["gastar"] = sum(originDict["histGastar"])
    # expected gastar this month

    originDict["expectedGastar"] = originDict["income"] * originDict["ratioGastar"] + originDict["extras"]
    # remaining gastar this month
    originDict["remainingGastar"] = originDict["expectedGastar"] - originDict["gastar"]
    # acomulated gastar in this month
    if originDict["remainingVivir"] > 0:
        originDict["acomulatedGastar"] = originDict["remainingGastar"] + originDict["remainingVivir"] * originDict["ratioGastar"] * 2
    else:
        originDict["acomulatedGastar"] = originDict["remainingGastar"] + originDict["remainingVivir"]

    # expected save this month
    originDict["expectedSave"] = originDict["income"] * originDict["ratioSave"]
    # real saves this month
    if originDict["remainingVivir"] > 0:
        originDict["save"] = originDict["expectedSave"] + originDict["remainingVivir"] * originDict["ratioSave"] * 2
    else:
        originDict["save"] = originDict["expectedSave"]
    originDict["save"] += sum(originDict["extraSaves"])

def calculateOffsets(originDict):
    offsetGastar = 0
    offsetSave = 0
    originAnio = int(originDict["anio"])
    originMes = int(originDict["mes"])
    allJsons = os.listdir("files/track/")
    for destJson in allJsons:
        destAnio = int(destJson.split("_")[0])
        destMes = int(destJson.split("_")[1].split(".")[0])
        if destAnio < originAnio or (destAnio == originAnio and destMes < originMes):
            f = open("files/track/" + destJson, "r")
            destDict = json.loads(f.read())

            offsetGastar += destDict["acomulatedGastar"]
            offsetSave += destDict["save"]
    originDict["offsetGastar"] = offsetGastar
    originDict["offsetSave"] = offsetSave

def cargarMes(anio, mes):
    f = open(f'files/track/{anio}_{mes}.json', "r")
    return json.loads(f.read())

def crearMes(anio, mes):
    allJsons = os.listdir("files/track")
    if f"{anio}_{mes}.json" not in allJsons:
        outDict = createDict(anio, mes)
        calculateVariables(outDict)
        calculateOffsets(outDict)
        print(outDict)

try:
    mainDict = cargarMes(currentAnio, currentMes)
except:
    mainDict = createDict(currentAnio, currentMes)

calculateVariables(mainDict)
calculateOffsets(mainDict)

running = True
pintar = True
selected = ""
number = ""
while running:

    for event in pygame.event.get():
        if pintar:
            # Reset
            font = "./files/JetBrainsMono-Regular.ttf"
            myfont = pygame.font.Font(font, 20)
            pygame.draw.rect(screen, negro, pygame.Rect(0, 0, 600, 800))

            # Income
            if selected == "income":
                colorRecuadro = amarillo
                resalto = 3
                colorFondoTitulo = amarillo
                colorTitulo = negro
            else:
                colorRecuadro = blanco
                resalto = 1
                colorFondoTitulo = negro
                colorTitulo = blanco
            pygame.draw.rect(screen, colorRecuadro, pygame.Rect(20, 20, 175, 100), resalto, border_radius=6)
            pygame.draw.rect(screen, colorFondoTitulo, pygame.Rect(25, 8, (12 * 6) + 10, 24), border_radius=3)
            label = myfont.render("income", True, colorTitulo)
            screen.blit(label, (30, 5))
            myfont = pygame.font.Font(font, 24)
            label = myfont.render(str(mainDict["income"]), True, colorRecuadro)
            screen.blit(label, (65, 35))
            label = myfont.render(str(mainDict["extras"]), True, amarillo)
            screen.blit(label, (75, 70))
            myfont = pygame.font.Font(font, 20)

            # Date

            colorRecuadro = violetaclaro
            resalto = 3
            colorFondoTitulo = violetaclaro
            colorTitulo = negro

            pygame.draw.rect(screen, colorRecuadro, pygame.Rect(212.5, 20, 175, 100), resalto, border_radius=6)
            pygame.draw.rect(screen, colorFondoTitulo, pygame.Rect(217.5, 8, (12 * 4) + 10, 24), border_radius=3)
            label = myfont.render("date", True, colorTitulo)
            screen.blit(label, (222.5, 5))
            myfont = pygame.font.Font(font, 24)
            label = myfont.render(str(mainDict["anio"]), True, violetaclaro)
            screen.blit(label, (265, 40))
            label = myfont.render(str(mes[mainDict["mes"]]), True, violetaclaro)
            screen.blit(label, (275, 70))
            myfont = pygame.font.Font(font, 20)
            # Save
            if selected == "ahorros":
                colorRecuadro = verde
                resalto = 3
                colorFondoTitulo = verde
                colorTitulo = negro
            else:
                colorRecuadro = blanco
                resalto = 1
                colorFondoTitulo = negro
                colorTitulo = blanco
            pygame.draw.rect(screen, colorRecuadro, pygame.Rect(405, 20, 175, 100), resalto, border_radius=6)
            pygame.draw.rect(screen, colorFondoTitulo, pygame.Rect(410, 8, (12 * 7) + 10, 24), border_radius=3)
            label = myfont.render("ahorros", True, colorTitulo)
            screen.blit(label, (415, 5))
            myfont = pygame.font.Font(font, 28)
            label = myfont.render(str(round(mainDict["save"],2)), True, verde)
            screen.blit(label, (445, 55))
            myfont = pygame.font.Font(font, 20)

            # Vivir
            if selected == "vivir":
                colorRecuadro = azul
                resalto = 3
                colorFondoTitulo = azul
                colorTitulo = negro
            else:
                colorRecuadro = blanco
                resalto = 1
                colorFondoTitulo = negro
                colorTitulo = blanco
            pygame.draw.rect(screen, colorRecuadro, pygame.Rect(20, 140, 275, 535), resalto, border_radius=6)
            pygame.draw.rect(screen, colorFondoTitulo, pygame.Rect(25, 128, (12 * 5) + 10, 24), border_radius=3)
            label = myfont.render("vivir", True, colorTitulo)
            screen.blit(label, (30, 125))
            myfont = pygame.font.Font(font, 24)
            label = myfont.render("/", True, blanco)
            screen.blit(label, (150, 170))
            label = myfont.render(str(mainDict["vivir"]), True, colorRecuadro)
            screen.blit(label, (150-(-3+15*len(str(mainDict["vivir"]))), 170))
            label = myfont.render(str(round(mainDict["expectedVivir"],2)), True, blanco)
            screen.blit(label, (165, 170))
            myfont = pygame.font.Font(font, 20)
            if mainDict["remainingVivir"]>100:
                colorRemaining=verde
            elif mainDict["remainingVivir"] > 0:
                colorRemaining = naranja
            else:
                colorRemaining=rojo
            label = myfont.render(str(round(mainDict["remainingVivir"],2)), True, colorRemaining)
            screen.blit(label, (165-15*float(len(str(round(mainDict["remainingVivir"],2)))/2), 200))
            pygame.draw.line(screen, blanco, [60, 230], [260, 230], 1)
            vivirHist=list(reversed(mainDict["histVivir"].copy()))
            # So hist doesnt overflow
            if len(vivirHist)>11:
                vivirHist=vivirHist[:11]
                vivirHist.append("...")
            # print hist
            for i in range(len(vivirHist)):
                label=myfont.render(str(vivirHist[i]), True, blanco)
                screen.blit(label, (165-15*float(len(str(vivirHist[i]))/2), 250+i*35))

            # Gastar
            if selected == "gastar":
                colorRecuadro = cyan
                resalto = 3
                colorFondoTitulo = cyan
                colorTitulo = negro
            else:
                colorRecuadro = blanco
                resalto = 1
                colorFondoTitulo = negro
                colorTitulo = blanco
            pygame.draw.rect(screen, colorRecuadro, pygame.Rect(305, 140, 275, 535), resalto, border_radius=6)
            pygame.draw.rect(screen, colorFondoTitulo, pygame.Rect(310, 128, (12 * 6) + 10, 24), border_radius=3)
            label = myfont.render("gastar", True, colorTitulo)
            screen.blit(label, (315, 125))

            # Consola
            pygame.draw.rect(screen, azul, pygame.Rect(0, 695, 300, 25))

            pygame.display.update()
            pintar = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "i":
                selected = "income"
                number = ""
                pintar = True
            elif pygame.key.name(event.key) == "a":
                selected = "ahorros"
                number = ""
                pintar = True
            elif pygame.key.name(event.key) == "v":
                selected = "vivir"
                number = ""
                pintar = True
            elif pygame.key.name(event.key) == "g":
                selected = "gastar"
                number = ""
                pintar = True
            elif pygame.key.name(event.key) == "c":
                selected = ""
                number = ""
                pintar = True
            elif pygame.key.name(event.key) == "backspace":
                number = number[:-1]
                pintar = True
            elif pygame.key.name(event.key) == "return":
                # todo make functionality
                selected = ""
                number = ""
                pintar = True
            else:
                number += pygame.key.name(event.key)
                pintar = True
            # print(pygame.key.name(event.key))
            # pygame.display.update()
        elif event.type == pygame.QUIT:
            running = False
