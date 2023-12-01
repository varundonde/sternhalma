from main_121 import * 
from player_121 import * 
import math
import random
import copy

# CITATION: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
# Minimax inspiration came from my mentor Peter, and this YouTube video: https://www.youtube.com/watch?v=l-hh51ncgDI&t=120s&ab_channel=SebastianLague

def calculateMinimax(board):

    weightedBoard1 = [[None, None, None, None, None, 20, None, None, None, None, None], 
                     [None, None, None, None, 20, None, 20, None, None, None, None],
                     [None, None, None, 20, None, 20, None, 20, None, None, None],
                     [None, None, 15, None, 19, None, 19, None, 15, None, None], 
                     [None, 10, None, 14, None, 17, None, 14, None, 10, None], 
                     [6, None, 10, None, 16, None, 16, None, 10, None, 6], 
                     [None, 4, None, 8, None, 12, None, 8, None, 4, None], 
                     [None, None, 2, None, 6 , None, 6, None, 2, None, None], 
                     [None, None, None, 0, None, 0, None, 0, None, None, None],
                     [None, None, None, None, 0, None, 0, None, None, None, None], 
                     [None, None, None, None, None, 0, None, None, None, None, None]]
    
    weightedBoard2 = [[None, None, None, None, None, 0, None, None, None, None, None], 
                     [None, None, None, None, 0, None, 0, None, None, None, None],
                     [None, None, None, 0, None, 0, None, 0, None, None, None],
                     [None, None, 2, None, 6, None, 6, None, 2, None, None], 
                     [None, 4, None, 8, None, 12, None, 8, None, 4, None], 
                     [6, None, 10, None, 16, None, 16, None, 10, None, 6], 
                     [None, 10, None, 14, None, 17, None, 14, None, 10, None], 
                     [None, None, 15, None, 19, None, 19, None, 15, None, None], 
                     [None, None, None, 20, None, 20, None, 20, None, None, None],
                     [None, None, None, None, 20, None, 20, None, None, None, None], 
                     [None, None, None, None, None, 20, None, None, None, None, None]]

    playerOne = 0
    playerTwo = 0

    legalSquares = [(0, 5), (1, 4), (1, 6), (2, 3), (2, 5), (2, 7), 
                    (3, 2), (3, 4), (3, 6), (3, 8), (4, 1), (4, 3), 
                    (4, 5), (4, 7), (4, 9), (5, 0), (5, 2), (5, 4), 
                    (5, 6), (5, 8), (5, 10), (6, 1), (6, 3), (6, 5), 
                    (6, 7), (6, 9), (7, 2), (7, 4), (7, 6), (7, 8), 
                    (8, 3), (8, 5), (8, 7), (9, 4), (9, 6), (10, 5)]
    
    for coordinates in legalSquares:
        row, col = coordinates[0], coordinates[1]
        if board[row][col] == 1:
            playerOne += weightedBoard1[row][col]  
        elif board[row][col] == 2:
            playerTwo += weightedBoard2[row][col]
    print(f'Score Calculation: {playerOne}, {playerTwo}')
    return (playerOne, playerTwo)

# CITATION: Minimax Source Code found on Geeks for Geeks
# CITATION: Modified Source Code inspiration based on video mentioned above
    
def minimax_max(app, board, currDepth, targetDepth, player):
    if currDepth >= targetDepth:
        scores = calculateMinimax(board)
        if player == app.player1:
            return scores[0] - scores[1]
        elif player == app.player2:
            return scores[1] - scores[0]
            
    else:
        if player.number == 1:
            opponent = app.player2
        else:
            opponent = app.player1
        
        maxScore = -99999
        for piece in player.getPieces(board):
            print(f'Current Max Piece: {piece}')
            movelist = player.getPossibleMoveListForPiece(piece, board)
            for move in movelist:
                newState = player.makeMove(piece, move[0], move[1], board)
                score = minimax_min(app, newState, currDepth + 1, targetDepth, opponent)
                print(score)
                if score > maxScore:
                    maxScore = score
        print(maxScore)
        return maxScore 
        
    
def minimax_min(app, board, currDepth, targetDepth, player):
    if currDepth >= targetDepth:
        scores = calculateMinimax(board)
        if player == app.player1:
            return scores[0] - scores[1]
        elif player == app.player2:
            return scores[1] - scores[0]
    else:
        if player.number == 1:
            opponent = app.player2
        else:
            opponent = app.player1
        
        minScore = 99999
        
        for piece in player.getPieces(board):
            print(f'Current Min Piece: {piece}')
            movelist = player.getPossibleMoveListForPiece(piece, board)
            for move in movelist:
                newState = player.makeMove(piece, move[0], move[1], board)
                score = minimax_max(app, newState, currDepth + 1, targetDepth, opponent)
                print(score)
                if score < minScore:
                    minScore = score
        print(minScore)
        return minScore
        


def minimaxPlay(app, player):
    board = copy.deepcopy(app.playerBoard)
    if player == app.player1:
        opponent = app.player2
    else:
        opponent = app.player1
    
    maxScore = -99999
    bestMove = None
    bestPiece = None
    for piece in player.piecesList:
        movelist = player.getPossibleMoveListForPiece(piece, board)
        for move in movelist:
            newState = player.makeMove(piece, move[0], move[1], board)
            score = minimax_max(app, newState, 0, 2, player)
            
            if score > maxScore:
                maxScore = score
                bestMove = move
                bestPiece = piece
                print(bestPiece)
                print(maxScore)
                print(bestMove)
                
                
    app.turn.gameOver(app, board, app.turn)
    if not app.gameOver:
        newBoard = player.makeMove(bestPiece, bestMove[0], bestMove[1], app.playerBoard)
        if app.turn == app.player1:
            app.turn = app.player2
        else:
            app.turn = app.player1

    app.playerBoard = copy.deepcopy(newBoard)
    return app.playerBoard
    







    
    