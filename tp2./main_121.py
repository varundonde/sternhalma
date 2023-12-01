from cmu_graphics import *
import math
import copy
from player_121 import *
from randomAI_121 import *
from minimax_121 import *

def onAppStart(app):
    app.width = 440 
    app.height = 440
    app.rows = 11
    app.cols = 11
    app.boardLeft = 0
    app.boardTop = 0
    app.boardWidth = app.width 
    app.boardHeight = app.height 
    app.cellBorderWidth = 4
    

    app.endZone1 = [(0, 5), (1, 4), (1, 6), (2, 3), (2, 5), (2, 7)]
    app.endZone2 = [(8, 3), (8, 5), (8, 7), (9, 4), (9, 6), (10, 5)]
    
    app.copyBoard = [[3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3], 
                     [3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 3],
                     [3, 3, 3, 2, 3, 2, 3, 2, 3, 3, 3],
                     [3, 3, 0, 3, 0, 3, 0, 3, 0, 3, 3], 
                     [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3], 
                     [0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0], 
                     [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3], 
                     [3, 3, 0, 3, 0, 3, 0, 3, 0, 3, 3], 
                     [3, 3, 3, 1, 3, 1, 3, 1, 3, 3, 3],
                     [3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3], 
                     [3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3]]
    
    app.playerBoard = [[3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3], 
                       [3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 3],
                       [3, 3, 3, 2, 3, 2, 3, 2, 3, 3, 3],
                       [3, 3, 0, 3, 0, 3, 0, 3, 0, 3, 3], 
                       [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3], 
                       [0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0], 
                       [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3], 
                       [3, 3, 0, 3, 0, 3, 0, 3, 0, 3, 3], 
                       [3, 3, 3, 1, 3, 1, 3, 1, 3, 3, 3],
                       [3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3], 
                       [3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3]]
    
    app.player1 = Player(1, app.playerBoard)
    app.player2 = Player(2, app.playerBoard)
    app.player1.pieces = app.player1.getPieces(app.playerBoard)
    app.player2.pieces = app.player2.getPieces(app.playerBoard)
    app.turn = app.player1
    app.gameOver = False
    app.multiplayer = False
    app.aiScreen = False
    app.selected = None
    app.home = True
    app.minimax = False
    app.random = False

# AI Method

def playAI(app):
    if app.minimax:
        print("AI STARTED")
        if app.turn == app.player2:
            print("TURN CORRECT")
            minimaxPlay(app, app.player2)
    elif app.random == True:
        print("RANDOM STARTED")
        if app.turn == app.player2:
            randomAI(app, app.player2)

# Essential Methods 

def redrawAll(app):
    if app.home:
        drawHome(app)
    
    elif app.aiScreen:
        drawAI(app)
        
    elif not app.home and not app.aiScreen:
        drawBoard(app)
        drawPieces(app)
        if app.selected != None:
            drawPotentialPositions(app, app.selected)
        if app.gameOver:
            drawMessage(app)


def onMousePress(app, mouseX, mouseY):
    if app.home:
        if 35 <= mouseX <= 185 and 305 <= mouseY <= 355:
            app.home = False
            app.aiScreen = True
        elif 255 <= mouseX <= 405 and 305 <= mouseY <= 355:
            app.home = False
            app.multiplayer = True
    
    elif app.aiScreen:
        if 35 <= mouseX <= 185 and 305 <= mouseY <= 355:
            app.aiScreen = False
            app.multiplayer = True
            app.minimax = True
        elif 255 <= mouseX <= 405 and 305 <= mouseY <= 355:
            app.aiScreen = False
            app.random = True
            app.multiplayer = True


    if not app.gameOver and app.multiplayer:
        if app.selected == None:
            interestCell = getCell(app, mouseX, mouseY)
            if interestCell != None:
                piecesList = app.turn.getPieces(app.playerBoard)
                if interestCell in piecesList:
                    app.selected = interestCell
                    #print(f'{app.selected} selected piece!')
                    #print(f'possible moves: {app.turn.getPossibleMoveListForPiece(app.selected, app.playerBoard)}')
        else:
            movingTo = getCell(app, mouseX, mouseY)
            if isLegal(app, app.turn, movingTo, app.selected):
                app.turn.makeMove(app.selected, movingTo[0], movingTo[1], app.playerBoard)
                app.turn.gameOver(app, app.playerBoard, app.turn)
                app.turn.pieces = app.turn.getPieces(app.playerBoard) 
                #print(f'New pieces after move are: {app.turn.getPieces(app.playerBoard)}')
                if app.turn == app.player1:
                    app.turn = app.player2

                else:
                    app.turn = app.player1
            
                playAI(app)
            
        
            
            app.player1.pieces = app.player1.getPieces(app.playerBoard)
            app.player2.pieces = app.player2.getPieces(app.playerBoard)
            app.selected = None
            
# backend Helpers

def isLegal(app, player, nextSquare, currSquare):
    piecesList = player.getPossibleMoveListForPiece(currSquare, app.playerBoard)
    if nextSquare in piecesList:
        return True
    else:
        return False

# CITATION - 15-112 Student Soham Khatavkar helped me come up with the idea to swtich from coordinate axis to board indices rather than creating psuedo board
def getCell(app, x, y):
    col = x // getCellSize(app)[0]
    row = y // getCellSize(app)[1]
    if app.playerBoard[row][col] != 3:
        return (row, col)
    else:
        return None

def cellSize(app):
    return (((getCellSize(app)[0] ** 2) + (getCellSize(app)[1] ** 2)) ** 0.5)

# Drawing Helpers

def drawHome(app):
    drawRect(0, 0, app.boardWidth, app.boardHeight, fill = "Brown")
    drawLabel("Welcome to Sternhalma.", 220, 100, size = 30, align = 'center', font = 'monospace', fill = 'white', bold = True)
    drawLabel("Play vs AI.", 110, 330, size = 20, align = 'center', font = 'monospace', fill = 'white')
    drawLabel("Multiplayer.", 330, 330, size = 20, align = 'center', font = 'monospace', fill = 'white')
    drawRect(110, 330, 150, 50, fill = None, border = 'white', borderWidth = 2, align = 'center')
    drawRect(330, 330, 150, 50, fill = None, border = 'white', borderWidth = 2, align = 'center')

def drawAI(app):
    drawRect(0, 0, app.boardWidth, app.boardHeight, fill = "Brown")
    drawLabel("Choose an option below.", 220, 100, size = 30, align = 'center', font = 'monospace', fill = 'white', bold = True)
    drawLabel("vs Minimax.", 110, 330, size = 20, align = 'center', font = 'monospace', fill = 'white')
    drawLabel("vs Random.", 330, 330, size = 20, align = 'center', font = 'monospace', fill = 'white')
    drawRect(110, 330, 150, 50, fill = None, border = 'white', borderWidth = 2, align = 'center')
    drawRect(330, 330, 150, 40, fill = None, border = 'white', borderWidth = 2, align = 'center')

def drawMessage(app):
    if app.turn == app.player2:
        drawLabel(f'Player 1 Wins', 220, 220, fill = 'red', size = 18)
    else:
        drawLabel(f'Player 2 Wins', 220, 220, fill = 'red', size = 18)

def drawPotentialPositions(app, piece):
    potentialPieces = app.turn.getPossibleMoveListForPiece(piece, app.playerBoard)
    for piece in potentialPieces:
        drawCell(app, piece[0], piece[1], 'lightGreen')

def drawPieces(app):
    for row in range(len(app.playerBoard)):
        for col in range(len(app.playerBoard[0])):
            if (row, col) in app.player1.pieces:
                drawCell(app, row, col, 'red')
            elif (row, col) in app.player2.pieces:
                drawCell(app, row, col, 'blue')

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.playerBoard[row][col] == 0 or app.playerBoard[row][col] == 2 or app.playerBoard[row][col] == 1:
                drawCell(app, row, col, None)

def drawBoardBorder(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, None)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
            fill = color, border='black',
            borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth // (app.cols)
    cellHeight = app.boardHeight // app.rows
    return (cellWidth, cellHeight)

# Minimax Helper



def main():
    runApp()

if __name__ == "__main__":
    main()
