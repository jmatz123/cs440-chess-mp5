import math
import sys

# from numpy import choose
import chess.lib
from chess.lib.utils import encode, decode
from chess.lib.heuristics import evaluate
from chess.lib.core import makeMove, move

###########################################################################################
# Utility function: Determine all the legal moves available for the side.
# This is modified from chess.lib.core.legalMoves:
#  each move has a third element specifying whether the move ends in pawn promotion
def generateMoves(side, board, flags):
    for piece in board[side]:
        fro = piece[:2]
        for to in chess.lib.availableMoves(side, board, piece, flags):
            promote = chess.lib.getPromote(None, side, board, fro, to, single=True)
            yield [fro, to, promote]
            
###########################################################################################
# Example of a move-generating function:
# Randomly choose a move.
def random(side, board, flags, chooser):
    '''
    Return a random move, resulting board, and value of the resulting board.
    Return: (value, moveList, boardList)
      value (int or float): value of the board after making the chosen move
      moveList (list): list with one element, the chosen move
      moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
    Input:
      side (boolean): True if player1 (Min) plays next, otherwise False
      board (2-tuple of lists): current board layout, used by generateMoves and makeMove
      flags (list of flags): list of flags, used by generateMoves and makeMove
      chooser: a function similar to random.choice, but during autograding, might not be random.
    '''
    moves = [ move for move in generateMoves(side, board, flags) ]
    if len(moves) > 0:
        move = chooser(moves)
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        value = evaluate(newboard)
        return (value, [ move ], { encode(*move): {} })
    else:
        return (evaluate(board), [], {})

###########################################################################################
# Stuff you need to write:
# Move-generating functions using minimax, alphabeta, and stochastic search.

# moveTree = {}
# moveList_result = []
def minimax(side, board, flags, depth):
  # https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/
    '''
    Return a minimax-optimal move sequence, tree of all boards evaluated, and value of best path.
    Return: (value, moveList, moveTree)
      value (float): value of the final board in the minimax-optimal move sequence
      moveList (list): the minimax-optimal move sequence, as a list of moves
      moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
    Input:
      side (boolean): True if player1 (Min) plays next, otherwise False
      board (2-tuple of lists): current board layout, used by generateMoves and makeMove
      flags (list of flags): list of flags, used by generateMoves and makeMove
      depth (int >=0): depth of the search (number of moves)
    '''
    
    # move: [fro,to,promote]
    # fro: [x,y]
    # to: [x,y]
    # move_value_dict = {}
    best_moveList = []
    best_move_fro = []
    best_move_to = []
    best_move = [best_move_fro, best_move_to, None]

    if depth == 0 :
      return evaluate(board), [], {}
    
    moves = [ move for move in generateMoves(side, board, flags) ] #generate list of possible moves
    if side == False : #player0(white)
      moveTree = {}
      value = -sys.maxsize

      for move in moves :
        new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
        val_result_of_minmax, moveList, moveTree_inner = minimax(new_side, new_board, new_flags, depth - 1)

        if val_result_of_minmax > value : #find the best move
          best_move = move
          best_moveList = moveList
          value = val_result_of_minmax

        moveTree[encode(*move)] = moveTree_inner

    else : #player1(black)
      moveTree = {}
      value = sys.maxsize 

      for move in moves :
        new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
        val_result_of_minmax, moveList, moveTree_inner = minimax(new_side, new_board, new_flags, depth - 1)

        if val_result_of_minmax < value: #find the best move
          best_move = move
          best_moveList = moveList
          value = val_result_of_minmax

        moveTree[encode(*move)] = moveTree_inner

    best_moveList.insert(0, best_move)
    return value, best_moveList, moveTree

def alphabeta(side, board, flags, depth, alpha=-math.inf, beta=math.inf):
    '''
    Return minimax-optimal move sequence, and a tree that exhibits alphabeta pruning.
    Return: (value, moveList, moveTree)
      value (float): value of the final board in the minimax-optimal move sequence
      moveList (list): the minimax-optimal move sequence, as a list of moves
      moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
    Input:
      side (boolean): True if player1 (Min) plays next, otherwise False
      board (2-tuple of lists): current board layout, used by generateMoves and makeMove
      flags (list of flags): list of flags, used by generateMoves and makeMove
      depth (int >=0): depth of the search (number of moves)
    '''

    best_moveList = []
    best_move_fro = []
    best_move_to = []
    best_move = [best_move_fro, best_move_to, None]

    if depth == 0 :
      return evaluate(board), [], {}
    
    moves = [ move for move in generateMoves(side, board, flags) ] #generate list of possible moves
    if side == False : #player0(white)
      moveTree = {}
      value = -sys.maxsize

      for move in moves :
        new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
        val_result_of_minmax, moveList, moveTree_inner = minimax(new_side, new_board, new_flags, depth - 1)

        if val_result_of_minmax > value : #find the best move
          best_move = move
          best_moveList = moveList
          value = val_result_of_minmax
        
        alpha = max(alpha, value)

        if value >= beta:
          break

        moveTree[encode(*move)] = moveTree_inner

    else : #player1(black)
      moveTree = {}
      value = sys.maxsize 

      for move in moves :
        new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
        val_result_of_minmax, moveList, moveTree_inner = minimax(new_side, new_board, new_flags, depth - 1)

        if val_result_of_minmax < value: #find the best move
          best_move = move
          best_moveList = moveList
          value = val_result_of_minmax

        beta = min(beta, value)

        if value <= alpha :
          break

        moveTree[encode(*move)] = moveTree_inner

    best_moveList.insert(0, best_move)
    print(moveTree)
    return value, best_moveList, moveTree
    

def stochastic(side, board, flags, depth, breadth, chooser):
    '''
    Choose the best move based on breadth randomly chosen paths per move, of length depth-1.
    Return: (value, moveList, moveTree)
      value (float): average board value of the paths for the best-scoring move
      moveLists (list): any sequence of moves, of length depth, starting with the best move
      moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
    Input:
      side (boolean): True if player1 (Min) plays next, otherwise False
      board (2-tuple of lists): current board layout, used by generateMoves and makeMove
      flags (list of flags): list of flags, used by generateMoves and makeMove
      depth (int >=0): depth of the search (number of moves)
      breadth: number of different paths 
      chooser: a function similar to random.choice, but during autograding, might not be random.
    '''
    raise NotImplementedError("you need to write this!")
