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
    
    app.cx = app.width / 2
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
    app.sliderScreen = False
    app.player1score = 0 
    app.player2score = 0
    app.sliderX = 0

# AI Method

def playAI(app):
    if app.minimax:
        if app.turn == app.player2:
            move_AI = minimaxPlay(app, app.player2)
            if isLegal(app, app.turn, move_AI[1], move_AI[0]):
                app.turn.makeMove(move_AI[0], move_AI[1][0], move_AI[1][1], app.playerBoard)
                app.turn = app.player1
    elif app.random == True:
        if app.turn == app.player2:
            randomAI(app, app.player2)

# Essential Methods 

def redrawAll(app):
    if app.home:
        drawHome(app)
    
    elif app.aiScreen:
        drawAI(app)

    elif app.sliderScreen:
        drawSliderScreen(app)
        
    elif not app.home and not app.aiScreen:
        drawRect(0, 0, app.boardWidth, app.boardHeight, fill = "Brown")
        drawBoard(app)
        drawPieces(app)
        drawScore(app)
        
        if app.selected != None:
            drawPotentialPositions(app, app.selected)
            drawLongJumps(app)
        if app.gameOver:
            drawMessage(app)

def onKeyPress(app, key):
    if app.gameOver:
        if key == 'r':
            app.playerBoard = copy.deepcopy(app.copyBoard)
            app.gameOver = False
            app.turn = app.player1
            app.player1.pieces = app.player1.getPieces(app.playerBoard)
            app.player2.pieces = app.player2.getPieces(app.playerBoard)
            app.player1score = 0 
            app.player2score = 0
        elif key == 'h':
            app.playerBoard = copy.deepcopy(app.copyBoard)
            app.turn = app.player1
            app.player1.pieces = app.player1.getPieces(app.playerBoard)
            app.player2.pieces = app.player2.getPieces(app.playerBoard)
            app.gameOver = False
            app.multiplayer = False
            app.aiScreen = False
            app.selected = None
            app.home = True
            app.minimax = False
            app.random = False
            app.home = True
            app.gameOver = False
            app.player1score = 0 
            app.player2score = 0
            app.cx = app.width / 2
            app.sliderX = 0
    elif not app.gameOver and key == 'b':
        app.playerBoard = copy.deepcopy(app.copyBoard)
        app.turn = app.player1
        app.player1.pieces = app.player1.getPieces(app.playerBoard)
        app.player2.pieces = app.player2.getPieces(app.playerBoard)
        app.gameOver = False
        app.multiplayer = False
        app.aiScreen = False
        app.selected = None
        app.home = True
        app.minimax = False
        app.random = False
        app.home = True
        app.gameOver = False
        app.player1score = 0 
        app.player2score = 0
        app.cx = app.width / 2
        app.sliderX = 0
    

def onMouseDrag(app, mouseX, mouseY):
    if 55 < mouseX < 385:
        app.cx = mouseX

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
            app.sliderScreen = True
        elif 255 <= mouseX <= 405 and 305 <= mouseY <= 355:
            app.aiScreen = False
            app.random = True
            app.multiplayer = True

    elif app.sliderScreen:
        if 55 <= mouseX <= 385 and 310 <= mouseY <= 350:
            if 55 <= mouseX < 165:
                app.sliderX = 1
            elif 165 <= mouseX < 275:
                app.sliderX = 2
            else:
                app.sliderX = 3
            app.sliderScreen = False
            app.multiplayer = True
            app.minimax = True

    else:
        if not app.gameOver and app.multiplayer:
            if app.selected == None:
                interestCell = getCell(app, mouseX, mouseY)
                if interestCell != None:
                    piecesList = app.turn.getPieces(app.playerBoard)
                    if interestCell in piecesList:
                        app.selected = interestCell     
                                  
            else:
                movingTo = getCell(app, mouseX, mouseY)
                if isLegal(app, app.turn, movingTo, app.selected):
                    app.turn.makeMove(app.selected, movingTo[0], movingTo[1], app.playerBoard)
                    app.turn.gameOver(app, app.playerBoard, app.turn)
                    app.turn.pieces = app.turn.getPieces(app.playerBoard) 

                    if app.turn == app.player1:
                        app.turn = app.player2

                    else:
                        app.turn = app.player1
                
                    playAI(app)
            
        
                calculateEndScore(app)
                app.player1.pieces = app.player1.getPieces(app.playerBoard)
                app.player2.pieces = app.player2.getPieces(app.playerBoard)
                app.selected = None
                

# drawing helper

def drawLongJumps(app):
    pathList = copy.deepcopy(app.turn.possibleJumps(app.playerBoard, app.selected))
    for path in pathList: 
        i = 0 
        while i < len(path) - 1:
            j = i + 1
            root = path[i] 
            destination = path[j]
            rootCoords, destinationCoords = getCoords(app, root[0], root[1]), getCoords(app, destination[0], destination[1])
            drawLine(rootCoords[0], rootCoords[1], destinationCoords[0], destinationCoords[1], fill = 'white', dashes = True, arrowEnd = True, lineWidth = 4)
            i += 1


# backend Helpers

def isLegal(app, player, nextSquare, currSquare):
    piecesList = player.getPossibleMoveListForPiece(currSquare, app.playerBoard)
    if nextSquare in piecesList:
        return True
    else:
        return False
    

def calculateEndScore(app):
    app.player1score = 0
    app.player2score = 0

    for coords in app.endZone1:
        row, col = coords[0], coords[1]
        if app.playerBoard[row][col] == 1:
            app.player1score += 1

    for coords2 in app.endZone2:
        row, col = coords2[0], coords2[1]
        if app.playerBoard[row][col] == 2:
            app.player2score += 1 

# CITATION - 15-112 Student Soham Khatavkar helped me come up with the idea to swtich from coordinate axis to board indices rather than creating psuedo board

def getCell(app, x, y):
    col = x // getCellSize(app)[0]
    row = y // getCellSize(app)[1]
    if app.playerBoard[row][col] != 3:
        return (row, col)
    else:
        return None
    
def getCoords(app, row, col):
    x = getCellSize(app)[0] * col + 20
    y = (getCellSize(app)[1] * row) + 20
    coord = (x,y)
    return coord

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2) ** 2 + (y1-y2) ** 2)
    
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
    drawRect(330, 330, 150, 50, fill = None, border = 'white', borderWidth = 2, align = 'center')

def drawSliderScreen(app):
    drawRect(0, 0, app.boardWidth, app.boardHeight, fill = "Brown")
    drawLabel("Drag slider to set minimax difficulty.", app.width / 2, app.height * 0.25, size = 16, align = 'center', font = 'monospace', fill = 'white', bold = True)
    drawLabel("Continue at set difficulty.", app.width / 2, app.height * 0.75, size = 20, align = 'center', font = 'monospace', fill = 'white', bold = True)
    drawRect(app.width / 2, app.height / 2, app.width * 0.75, 20, fill = 'black', align = 'center')
    drawCircle(app.cx, app.height / 2, 25, fill = 'black')
    drawRect(app.width / 2, app.height * 0.75, app.width * 0.75, 40, fill = None, border = 'white', borderWidth = 2, align = 'center')




def drawMessage(app):
    drawRect(0,0,app.boardWidth, app.boardHeight, fill = 'Brown')
    endScreen = rgb(147, 197, 120)
    drawRect(app.boardWidth / 2, app.boardHeight / 2, app.boardWidth / 2, app.boardHeight / 2, fill = endScreen, opacity = 50, border = 'black', borderWidth = 1, align = 'center')
    if app.turn == app.player2 and not app.minimax and not app.random:
        drawLabel('Player 1 Wins!', 220, 220, fill = 'white', size = 25, font = 'monospace')
    elif app.turn == app.player1 and not app.minimax and not app.random:
        drawLabel('Player 2 Wins!', 220, 220, fill = 'white', size = 25, font = 'monospace')
    elif app.turn == app.player2 and app.minimax:
        drawLabel('Player 2 Wins!', 220, 220, fill = 'white', size = 25, font = 'monospace')
    elif app.turn == app.player1 and app.minimax:
        drawLabel('Player 1 Wins!', 220, 220, fill = 'white', size = 25, font = 'monospace')
    drawLabel('Press r to restart', 220, 150, fill = 'white', size = 18, font = 'monospace')
    drawLabel('Press h to go home', 220, 175, fill = 'white', size = 14, font = 'monospace')

def drawScore(app):
    drawLabel(f'Player 1 Score: {app.player1score}', 85, 410, fill = 'white', size = 14, font = 'grenze')
    drawLabel(f'Player 2 Score: {app.player2score}', 85, 30, fill = 'white', size = 14, font = 'grenze')
    drawLabel(f'*Press b to go home', 375, 50, fill = 'white', size = 12, font = 'grenze')

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

# Main

def main():
    runApp()

if __name__ == "__main__":
    main()
