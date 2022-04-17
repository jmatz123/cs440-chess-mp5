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
    
    # for move in moves :
    #   print(encode(*move), "*****")
    # while depth > 0 :
    #   moves = [ move for move in generateMoves(side, board, flags) ] #generate list of possible moves
    #   for move in moves :
    #     new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
    #     # board_value = new_board
    #     # if minimax(new_side, new_board, new_flags, depth - 1) != None :
    #     value, moveList, moveTree_inner = minimax(new_side, new_board, new_flags, depth - 1)
    #       # print(value)
    #     moveTree[encode(*move)] = moveTree_inner
        # print(value, "xxxxxxx")
        

        
        # move_value_dict[encode(*move)] = value

        # if side == False : #player0 moves next
        #   max_move = max(move_value_dict, key = move_value_dict.get)
        #   # print("1", max_move)

        # else : #player1 moves next
        #   max_move = min(move_value_dict, key = move_value_dict.get)
        
        # new_side, new_board, new_flags = makeMove(side, board, max_move[0], max_move[1], flags, max_move[2])

        # minimax(new_side, new_board, new_flags, depth - 1)

    # return value, moveList, moveTree
    # print(moveTree)
        

      
    


    

    # while (depth > 0) :
    #   moves = [ move for move in generateMoves(side, board, flags) ] #generate list of possible moves
    #   for move in moves :
    #     minimax(side, board, flags, depth)
    #   # if side == False : #player0 moves next
    #   #   # return optimal list of moves as moveList

    #   # figure out how to choose which move to do
    #   for move in moves :
    #     print(encode(*move))
    #     new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
    #     value = evaluate(new_board)
    #     print(value)
    #     move_value_dict[encode(*move)] = value
    #     # moveTree_inner[encode(*move)] = {}
      
    #   # find move with greatest value
    #   if side == False : #player0 moves next
    #     # max_move = moves[3]
    #     max_move = max(move_value_dict, key = move_value_dict.get)
    #     print("1", max_move)
    #     # print_move = (decode(*max_move))
    #     # print(print_move)
    #   else : #player1 moves next
    #     max_move = min(move_value_dict, key = move_value_dict.get)
    #     print("2",max_move)
    #   # moveList.append(max_move)
    #   print("****", max_move)
    #   # print(decode(*max_move[0]))
    #   # print(max_move[1])
    #   # print(max_move[2])
    #   moveTree[encode(*max_move)] = moveTree_inner

    #   # make move with greatest value
    #   new_side, new_board, new_flags = makeMove(side, board, max_move[0], max_move[1], flags, max_move[2])
    #   depth = depth - 1

    #   # recurse
    #   minimax(new_side, new_board, new_flags, depth)
    #   # else : #player1 moves next
    #   #   # figure out how to choose which move to do
    #   #   for move in moves :
    #   #     new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
    #   #     value = evaluate(new_board)
    #   #     move_value_dict[move] = value
    #   #     moveTree_inner[encode(*move)] = {}
        
    #   #   # find move with lowest value
    #   #   min_move = min(move_value_dict, key = move_value_dict.get)
    #   #   moveList.append(min_move)
    #   #   moveTree[encode(*max_move)] = moveTree_inner

    #   #   # make move with greatest value
    #   #   new_side, new_board, new_flags = makeMove(side, board, min_move[0], min_move[1], flags, min_move[2])
    #   #   depth = depth - 1

    #   #   # recurse
    #   #   minimax(new_side, new_board, new_flags, depth)
      
    #   if depth == 1 :
    #     value_result = evaluate(new_board)
      
    #   # create moveList
    #   for key in moveTree :
    #     moveList.append(key)
    
    # return(value_result, moveList, moveTree)
    
    # raise NotImplementedError("you need to write this!")

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

    # moveTree = {}
    # if depth == 0 :
    #   return evaluate(board), [], {}
    
    # moves = [ move for move in generateMoves(side, board, flags) ] #generate list of possible moves
    # if side == False : #player0(white)
    #   value = -sys.maxsize

    #   for move in moves :
    #     new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
    #     val_result_of_alphabeta, moveList, moveTree_inner = alphabeta(new_side, new_board, new_flags, depth -1, alpha, beta)

    #     if val_result_of_alphabeta > value : #find the best move
    #       best_move = move
    #       value = val_result_of_alphabeta
        
    #     if value >+ beta :
    #       break

    #     alpha = max(alpha, value)
    #     moveTree[encode(*move)] = moveTree_inner
    #   moveList.append(best_move)

    #   return value, moveList, moveTree
    
    # else: #player1(black)
    #   value = sys.maxsize

    #   for move in moves :
    #     new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
    #     val_result_of_alphabeta, moveList, moveTree_inner = alphabeta(new_side, new_board, new_flags, depth -1, alpha, beta)

    #     if val_result_of_alphabeta < value : #find the best move
    #       best_move = move
    #       value = val_result_of_alphabeta
        
    #     if value <=alpha :
    #       break
        
    #     beta = min(beta, value)
    #     moveTree[encode(*move)] = moveTree_inner
    #   moveList.append(best_move)

    #   return value, moveList, moveTree
    # raise NotImplementedError("you need to write this!")
    

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
