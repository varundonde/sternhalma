from main_121 import *
import copy

class Player:
    
    def __init__(self, number, board, rows = 11, cols = 11):
        self.number = number
        self.board = board
        self.rows = rows
        self.cols = cols
        self.piecesList = []
        self.legalSquares = [(0, 5), (1, 4), (1, 6), (2, 3), (2, 5), (2, 7), 
                             (3, 2), (3, 4), (3, 6), (3, 8), (4, 1), (4, 3), 
                             (4, 5), (4, 7), (4, 9), (5, 0), (5, 2), (5, 4), 
                             (5, 6), (5, 8), (5, 10), (6, 1), (6, 3), (6, 5), 
                             (6, 7), (6, 9), (7, 2), (7, 4), (7, 6), (7, 8), 
                             (8, 3), (8, 5), (8, 7), (9, 4), (9, 6), (10, 5)]
        
        
    def __repr__(self):
        return f'Player Number: {self.number}'
    
    def getPieces(self, board):
        self.board = board
        self.piecesList = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == self.number:
                    newTuple = (row, col)
                    self.piecesList.append(newTuple)
        return self.piecesList

    def getNumber(self):
        return self.number
    
    def getPossibleMoveListForPiece(self, piece, board):
        self.board = board
        finalArray = []
        pieceRow, pieceCol = piece[0], piece[1]
        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 2), (0, -2)]
        for drow, dcol in dirs: # checks if any moves can be made from the piece's current position
            newRow, newCol = pieceRow + drow, pieceCol + dcol
            pair = (newRow, newCol)
            if pair in self.legalSquares:
                if self.board[newRow][newCol] == 0 and (newRow,newCol) not in self.piecesList:  
                # checks is the board is valid, and if the square is not occupied by the current player or other player's pieces
                    finalArray.append((newRow, newCol)) # appends
                else:
                    continue
        jumpsPerPiece = self.possibleJumps(board, piece)
        finalArray.extend(jumpsPerPiece)
    
        return finalArray
    
# Game Over Helper:
    def gameOver(self, app, board, player):
        self.board = board
        selfCount = 0
        otherCount = 0
        if player == app.player1:
            for searchTuple in app.endZone1:
                row, col = searchTuple[0], searchTuple[1]
                if board[row][col] == 1 and row <= 2:
                    selfCount += 1
                elif board[row][col] == 2 and row <= 2 :
                    otherCount += 1
        elif player == app.player2:
            for searchTuple in app.endZone2:
                row, col = searchTuple[0], searchTuple[1]
                if board[row][col] == 2 and row >= 9:
                    selfCount += 1
                elif board[row][col] == 1 and row >= 9:
                    otherCount += 1
    
        if otherCount == 6:
            app.gameOver = False
        else:
            if (otherCount + selfCount == 6) or selfCount == 6:
                app.gameOver = True
            
# The Jump Helper Trio: possibleJumps is a wrapper for dfsChain, which recursively finds all the possible positions to elsewhere
# within dfsChain, there is a helper method that calculates the jumps at a specified node, called jumpList
# jumpList does the legal checks for whether a jump can be made from a certain spot 

    def jumpList(self, piece, board, seen):
        self.board = board
        jumpSet = []
        pieceRow, pieceCol = piece[0], piece[1]
        dirs = [(-2, -2), (-2, 2), (2, -2), (2, 2), (0, -4), (0, 4)]
        for drow, dcol in dirs:
            newRow, newCol = pieceRow + drow, pieceCol + dcol
            pair = (newRow, newCol)
            if pair in self.legalSquares:
                if self.board[newRow][newCol] == 0 and not seen[newRow][newCol]: 
                    squareToJumpY, squareToJumpX = (pieceRow + (drow // 2), pieceCol + (dcol // 2))
                    if self.board[squareToJumpY][squareToJumpX] == 1 or self.board[squareToJumpY][squareToJumpX] == 2:
                        jumpCoords = (newRow, newCol)
                        jumpSet.append(jumpCoords)
                else:
                    continue
        if jumpSet == []:
            return None
        else:
            return jumpSet
    # CITATION: Implementation, ideas and general understanding of graph traversal found on YouTube: https://www.youtube.com/watch?v=PMMc4VsIacU&ab_channel=Reducible
    # CITATION: Geeks for Geeks DFS Source Code: https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/ (heavily edited in the case of jumping)
    # Diagram for understanding of graph provided on design documents for TP1
    def dfsChain(self, board, root, seen, jumps):
        self.board = board
        row, col = root[0], root[1]
        seen[row][col] = True

        jumpsFromPos = self.jumpList(root, self.board, seen)
        if jumpsFromPos != None:
            for jump in jumpsFromPos:
                jumpRow, jumpCol = jump[0], jump[1]
                newCoord = (jumpRow, jumpCol)
                jumps.append(newCoord)
                newRoot = (jumpRow, jumpCol)
                self.dfsChain(self.board, newRoot, seen, jumps)

    def possibleJumps(self, board, root):
        self.board = board
        seen = [[False for row in range(len(self.board))] for col in range(len(self.board[0]))]
        jumps = []
        self.dfsChain(self.board, root, seen, jumps)
        return jumps
    
    def makeMove(self, piece, row, col, board):
        self.board = board
        pieceRow, pieceCol = piece[0], piece[1]
        moveList = self.getPossibleMoveListForPiece(piece, self.board)
        if (row, col) in moveList:
            self.board[pieceRow][pieceCol] = 0
            self.board[row][col] = self.number
        
        return self.board
    
# Minimax Helpers:

    def pieceMappedToMoves(self, board):
        self.board = board
        mappedPieces = dict()
        for piece in self.piecesList:
            mappedPieces[piece] = self.getPossibleMoveListForPiece(piece, self.board)
        return mappedPieces
   
    def getPossibleMoves(self, board):
        self.board = board
        finalList = []
        for piece in self.piecesList:
            movesetForPiece = self.getPossibleMoveListForPiece(piece, self.board)
            finalList.append(movesetForPiece)
        
        moveArray = self.flatten(finalList)
        return moveArray
    
    def flatten(self, L):
        if L == []:
            return []
        else:
            curr = L[0]
            rest = L[1:]
            if isinstance(curr, list):
                return self.flatten(curr) + self.flatten(rest)
            else:
                return curr + self.flatten(rest)
    