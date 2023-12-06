from main_126 import *
from player_126 import *
import copy
import random

def randomAI(app, player):
    # check if it's the player's turn
    if app.turn == player:
        # save positions of all possible moves
        pieceIndex = random.randint(0, 5)
        pieceOfInterest = player.piecesList[pieceIndex]
        movesetForPiece = player.getPossibleMoveListForPiece(pieceOfInterest, app.playerBoard)
        moveIndex = random.randint(0, len(movesetForPiece) - 1)
        moveOfInterest = movesetForPiece[moveIndex]
        app.player2.makeMove(pieceOfInterest, moveOfInterest[0], moveOfInterest[1], app.playerBoard)
        app.turn = app.player1

        

        
