from main_927 import *
import copy

class Player:
    
    def __init__(self, number, board, rows = 11, cols = 11):
        self.number = number
        self.board = board
        self.rows = rows
        self.cols = cols
        self.piecesList = []
        
        
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
            if (0 <= newRow <= 11) and (0<= newCol <= 11):
                if self.board[newRow][newCol] == 0 and (newRow,newCol) not in self.piecesList:  
                # checks is the board is valid, and if the square is not occupied by the current player or other player's pieces
                    finalArray.append((newRow, newCol)) # appends
                else:
                    continue
        jumpsPerPiece = self.possibleJumps(board, piece)
        print(jumpsPerPiece)
        finalArray.extend(jumpsPerPiece)
    
        return finalArray
            
# The Jump Helper Trio: possibleJumps is a wrapper for dfsChain, which recursively finds all the possible positions to elsewhere
# within dfsChain, there is a helper method that calculates the jumps at a specified node, called jumpList
# jumpList does the legal checks for whether a jump can be made from a certain spot 

    def jumpList(self, piece, board, seen):
        self.board = board
        jumpSet = []
        pieceRow, pieceCol = piece[0], piece[1]
        dirs = [(-2, -2), (-2, 2), (2, -2), (2, 2), (0, -4), (0, 4)]
        for drow, dcol in dirs:
            print(drow, dcol)
            newRow, newCol = pieceRow + drow, pieceCol + dcol
            print(newRow, newCol)
            if (0 <= newRow <= 11) and (0<= newCol <= 11):
                if self.board[newRow][newCol] == 0 and not seen[newRow][newCol]: 
                    print(f'Evaluating Jump List: {(newRow, newCol)}')
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
