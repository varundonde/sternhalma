from cmu_graphics import *
import math
import copy
from player_927 import *

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
    app.selected = None

# Essential Methods 

def redrawAll(app):
    drawBoard(app)
    drawPieces(app)
    if app.selected != None:
        drawPotentialPositions(app, app.selected)
    

def onMousePress(app, mouseX, mouseY):
    if not app.gameOver:
        if app.selected == None:
            interestCell = getCell(app, mouseX, mouseY)
            if interestCell != None:
                piecesList = app.turn.getPieces(app.playerBoard)
                if interestCell in piecesList:
                    app.selected = interestCell
                    print(f'{app.selected} selected piece!')
                    print(f'possible moves: {app.turn.getPossibleMoveListForPiece(app.selected, app.playerBoard)}')
        else:
            movingTo = getCell(app, mouseX, mouseY)
            if isLegal(app, app.turn, movingTo, app.selected):
                app.turn.makeMove(app.selected, movingTo[0], movingTo[1], app.playerBoard)
                app.turn.pieces = app.turn.getPieces(app.playerBoard)
                print(f'New pieces after move are: {app.turn.getPieces(app.playerBoard)}')
                if app.turn == app.player1:
                    app.turn = app.player2
                else:
                    app.turn = app.player1
            
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

def drawPotentialPositions(app, piece):
    potentialPieces = app.turn.getPossibleMoveListForPiece(piece, app.playerBoard)
    for piece in potentialPieces:
        drawCell(app, piece[0], piece[1], 'lightGreen')

""" def drawPotentialHelper(app, row, col, board):
    drawCircle(row * getCellSize(app)[0], col * getCellSize(app)[1], 10, fill = 'lightGreen') """

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

def main():
    runApp()

if __name__ == "__main__":
    main()
