# This file is part was created originally by parzibyte.
# It appears to be free of licence, but you can check with the original source
# https://parzibyte.me/blog/2022/07/27/buscaminas-python-programacion-juego/
#
# Adapted to jocsCalamot by Pedro Bonilla.
#


import random
import requests
import unidecode
from termcolor import colored
from collections import defaultdict
import f00_functions as f00

# Editables per canviar el tipus de partida
numMines = 4  #Es pot editar per jugar taulells més grans
dictLeters = "ABCD" #Es pot editar per jugar taulells més grans
numRows = len(dictLeters)
numColumns = numRows #Es pot editar per jugar taulells no quadrats

# simbols globals inmutables
dictRows={0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F"}
symbolMine = "*"
symbolNotOpened = "."
symbolOpened = "-"

# Funcions
def inicializeBoard():
    global boardMatrix
    boardMatrix = []
    """
    Omple el taulell per primer cop
    """
    for row in range(numRows):
        boardMatrix.append([])
        for column in range(numColumns):
            boardMatrix[row].append(symbolNotOpened)
    return boardMatrix


def number2Letter(number):
    """
    Torna la lletra corresponent al número introduit
    """
    return dictLeters[number]


def letter2Number(letter):
    """
    Torna el número correspont a la lletra COMENÇANT EN 0. Per exemple
    A: 0
    B: 1
    """
    # Nota: si en algún momento se deseara que el tablero fuera más grande, solo sería cuestión de agregar más letras a la cadena
    number = dictLeters.index(letter)
    return number


def getIndexesFromCoordinates(coordinates):
    """
    Torna, a partir d'una coordenada (per exemple A1), les coordenades
    reals de la matriu; es a dir, els índex de l'array d'arrais. 
    Exemple, per a
    A1 tornarà [0, 0]
    """
    letter = coordinates[0:1]
    row = letter2Number(letter)
    column = int(coordinates[1:2]) - 1
    return row, column


def drawMinesInBoardFromList(listPositions, boardMatrix):
    for position in listPositions:
        row, column = getIndexesFromCoordinates(position)
        boardMatrix[row][column] = symbolMine
    return boardMatrix


def drawBoardFromString(positionsString, boardMatrix):
    # Convertimos a mayúscula para que podamos comparar de mejor manera
    positionsString = positionsString.upper()
    positionsSeparated = []
    primera_posicion = positionsString[0:2]
    segunda_posicion = positionsString[2:4]
    tercera_posicion = positionsString[4:6]
    if not primera_posicion in positionsSeparated:
        positionsSeparated.append(primera_posicion)
    if not segunda_posicion in positionsSeparated:
        positionsSeparated.append(segunda_posicion)
    if not tercera_posicion in positionsSeparated:
        positionsSeparated.append(tercera_posicion)
    boardMatrix = drawMinesInBoardFromList(positionsSeparated, boardMatrix)
    return boardMatrix


def startBoardListLists(listMines, boardMatrix):
    # Faig un loop per les mines per canviar el format
    # al que tenia el programa original
    for i in range(numMines):
        # Canvio l'input al format que hem demanen
        txtRow=dictRows[listMines[i][0]]
        txtCol=str(listMines[i][1])
        listMines[i]=txtRow + txtCol
    boardMatrix = drawMinesInBoardFromList(listMines, boardMatrix)
    return boardMatrix


def getCloseMines(row, column, boardMatrix):
    counter = 0
    if row <= 0:
        rowStart = 0
    else:
        rowStart = row - 1
    if row + 1 >= numRows:
        rowEnd = numRows - 1
    else:
        rowEnd = row + 1

    if column <= 0:
        columnStart = 0
    else:
        columnStart = column - 1

    if column + 1 >= numColumns:
        columnEnd = numColumns - 1
    else:
        columnEnd = column + 1

    for f in range(rowStart, rowEnd + 1):
        for c in range(columnStart, columnEnd + 1):
            # Si es la central, la omitim
            if f == row and c == column:
                continue
            if boardMatrix[f][c] == symbolMine:
                counter += 1
    return str(counter)


def printBoard(booleanWin, booleanLoss, boardMatrix):
    print("")
    lastTile = False
    # Imprimir cantonada superior esquerra
    print("  ", end="")
    # Imprimir resta de l'encapçalament
    for column in range(numColumns):
        print(str(column + 1), end=" ")
    # Salt de línea
    print("")
    # Imprimir contcontingut...
    numero_fila = 0
    for fila in boardMatrix:
        letra = number2Letter(numero_fila)
        print(letra, end=" ")
        for numero_columna, dato in enumerate(fila):
            # El tablero tiene los verdaderos datos, pero nosotros imprimimos otros para que el usuario no "descubra" lo que hay debajo
            trueSymbol = ""
            color = "white"
            if dato == symbolMine:
                if booleanWin or booleanLoss:
                    trueSymbol = symbolMine
                    color = "red"
                else:
                    trueSymbol = symbolNotOpened
            elif dato == symbolOpened:
                trueSymbol = getCloseMines(numero_fila, numero_columna,boardMatrix)
                if trueSymbol == "0":
                    color = "blue"
                elif trueSymbol == "1":
                    color = "green"
                elif trueSymbol == "2":
                    color = "yellow"
                elif trueSymbol == "3":
                    color = "magenta"
                elif trueSymbol == "4":
                    color = "red"
                elif trueSymbol == "5":
                    color = "red" 
            elif dato == symbolNotOpened:
                trueSymbol = "."
            print(colored(trueSymbol,color), end=" ")
        print("")
        numero_fila += 1


def openTile(coordinates, boardMatrix):
    booleanWin = False
    booleanLoss = False
    row, column = getIndexesFromCoordinates(coordinates)
    # Què hi havia en la casella?
    elementCurrent = boardMatrix[row][column]
    # Si hi ha una mina, perd i ja no es modifica res
    if elementCurrent == symbolMine:
        booleanWin = True
        #print("He cambiado HE PERDIDO A TRUE")
        return booleanLoss,booleanWin
    # Si hi ha un element sesnes obrir, l'obre
    if elementCurrent == symbolNotOpened:
        boardMatrix[row][column] = symbolOpened
    # Comprobem si hi ha caselles sense obrir o ja hem acabat
    if checkTilesToOpen(boardMatrix):
        booleanLoss = True   
    return booleanLoss,booleanWin


def checkTilesToOpen(boardMatrix):
    for fila in boardMatrix:
        for columna in fila:
            if columna == symbolNotOpened:
                return False
    return True


def askForCoordinates(): # Això ja no es fa servir, ho vaig canvia a aleatori
    while True:
        coordinates = input("Entra les posicions de les mines: ")
        if len(coordinates) == numColumns:
            return coordinates
        else:
            print("Coordenades no vàlidas. Torna-ho a intentar")


# La posició de les mines és automàtica
def createRandomBoard(numMines,numRows,numCol):
    # Declaro la llista on desare la posició de les mines
    listMines=[[-1,-1]]*numMines
    # Loop per totes les mines
    for i in range(numMines):
        # posició de la mina dolenta per intrar al while
        xy=[-1,-1]
        while xy in listMines:
            # Genero aleatòriament 
            xy=[random.randint(0,numRows-1),random.randint(0,numCol-1)]
            # Si esta repetida el while fara que s'en generi una altra
        listMines[i]=xy  
    return listMines  

def AskForTile():
    tileIsValid = False
    while not tileIsValid :
        tile = input("Quina casella del taulell vols obrir : ")
        tile = tile.upper()
        if len(tile) != 2:
            print("Has d'introduir una lletra i un número")
        elif not tile[0].isalpha():
            print("El primer valor ha de ser una lletra")
        elif not tile[1].isdigit():
            print("El segon valor ha de ser un número")
        elif not tile[0] in dictLeters:
            print("La lletra ha d'esta al rang " + dictLeters)
        elif int(tile[1]) <= 0 or int(tile[1]) > numColumns:
            print(f"El número ha d'estar al rang 1-{numColumns}")
        else:
            tileIsValid = True
        return tile


def startBuscamines():
    # Joc del Buscamines, FUNCIÓ PRINCIPAL
    # Defineixo un nom provisional pel jugador,
    # Després quan vingui la versió 2.0 l'haureu de canviar, 
    # perquè jo al carregador de jocs canviaré la manera com es defineix player
    booleanWin = False
    booleanLoss = False
    player = "Jugador" 
    print('\n Benvingut ' + player + '!!! \n Juguem al Buscamines')
    print('Al tauler s\'amagen ' + str(numMines) + ' mines')
    print('El jugador ha d\'anar seleccionant caselles a alliberar')
    print('si hi havia una mina, el jugador perd.')
    print('Si no, la casella mostra el núero de mines al seu voltant')
    print('Ho sento, però s\'han d\'alliberar totes les caselles 1 a 1, ¯\_(ツ)_/¯')
    print('No facis aquesta reacció a l\'institut -> (╯°□°）╯︵ ┻━┻')
    print("")
    # Variable a tornar per que el main general sàpiga que fer
    errorsInExecution = 0
    boardMatrix = inicializeBoard()
    #coordenadas = solicitar_coordenadas()
    listMines = createRandomBoard(numMines,numRows,numColumns)
    #iniciar_tablero_con_string(coordenadas )
    boardMatrix= startBoardListLists(listMines, boardMatrix)
    printBoard(booleanWin, booleanLoss, boardMatrix)
    while not booleanLoss and not booleanWin:
        tile = AskForTile()
        booleanWin,booleanLoss = openTile(tile, boardMatrix)
        printBoard(booleanWin, booleanLoss, boardMatrix)
        #print(booleanWin,booleanLoss) # Això ho tinc aquí per debugar
    # Per consistencia amb els jocs i el que demanaré a la versió 2
    # omplo winner en funció de si ha guanyat o perdut.
    if booleanWin:
        winner = True
    else:
        winner = False
    f00.messageEnd(winner, player)
    return errorsInExecution
    # Quan vingui la versió 2.0 aquí haureu d'afegir més coses al return


# Aquesta línia és només per comprobar que el programa et funciona sense el main
# Ja per la versió 1.0 hauries de comentar-la i passar-la al codi principal d'alguna manera.
if __name__ == "__main__":
    startBuscamines()
