import math
from os import pathsep
import sys

# from flask import Flask

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
        val_result_of_minmax, moveList, moveTree_inner = alphabeta(new_side, new_board, new_flags, depth - 1, alpha, beta)

        if val_result_of_minmax > value : #find the best move
          best_move = move
          best_moveList = moveList
          value = val_result_of_minmax
        
        moveTree[encode(*move)] = moveTree_inner
        if value >= beta:
          break

        alpha = max(alpha, value)

    else : #player1(black)
      moveTree = {}
      value = sys.maxsize 

      for move in moves :
        new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
        val_result_of_minmax, moveList, moveTree_inner = alphabeta(new_side, new_board, new_flags, depth - 1, alpha, beta)

        if val_result_of_minmax < value: #find the best move
          best_move = move
          best_moveList = moveList
          value = val_result_of_minmax
        
        moveTree[encode(*move)] = moveTree_inner

        if value <= alpha :
          break
          
        beta = min(beta, value)

    best_moveList.insert(0, best_move)
    # print(moveTree)
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
    # for every initial move, check breadth random paths
      # for each initial move, repeatedly use random chooser for depth -1 number of times
      # average the values of each path
      # find the move with the best average value(max for white and min for black)
    # if not an initial move, do random moves
    if depth == 0 :
        return evaluate(board), [], {}
    
    moveTree = {}
    moveList = []
    path_list = []
    
    init_move_vals = {}
    initial_moves = [ move for move in generateMoves(side, board, flags) ] #generate list of possible moves

    for init_move in initial_moves :
      average_value = 0

      # make initial move
      new_side, new_board, new_flags = makeMove(side, board, init_move[0], init_move[1], flags, init_move[2])
      # possible_moves = [ move for move in generateMoves(new_side, new_board, new_flags) ]

      initial_move_list = []
      counter_breadth = breadth
      total_init_move_value = 0
      while counter_breadth > 0 :
        # first move in path
        # next_move = chooser(possible_moves)
        # path_side, path_board, path_flags = makeMove(new_side, new_board, next_move[0], next_move[1], new_flags, next_move[2])

        last_side = new_side
        last_board = new_board
        last_flags = new_flags

        path_list = []
        counter_depth = depth
        while counter_depth - 1 > 0 :
          path_possible_moves = [ move for move in generateMoves(last_side, last_board, last_flags) ]
          path_move = chooser(path_possible_moves)
          path_list.insert(0, path_move)

          last_side, last_board, last_flags = makeMove(last_side, last_board, path_move[0], path_move[1], last_flags, path_move[2])
          # print("****",counter_breadth, counter_depth)
          counter_depth -= 1
        initial_move_list.append(path_list)

        leaf_val = evaluate(last_board)
        # print("leaf value", leaf_val)
        total_init_move_value += leaf_val
        # print("total value", total_init_move_value)
      
        counter_breadth -= 1
      
      multiple_path_coll = []
      some_dict = {}
      for big_list in initial_move_list :
        # print("big list", big_list)
        innerTree = {}

        for move in big_list :
          # print("inner tree:", innerTree)
          # innerDict = innerTree
          innerTree = {encode(*move) : innerTree}
          # innerTree[encode(*move)] = innerDict

        # print("final inner tree:", innerTree)
        multiple_path_coll.append(innerTree)
      for val in multiple_path_coll :
        some_dict = val | some_dict
        # print("multiple_path_coll", multiple_path_coll)
      moveTree[encode(*init_move)] = some_dict
      # print("movetree", moveTree)

      average_value = total_init_move_value / breadth
      # print("initial move", init_move)

      # print("average value", average_value)
      init_move_vals[encode(*init_move)] = average_value

    if side == False :
      best_move = max(init_move_vals, key=init_move_vals.get)
    else :
      best_move = min(init_move_vals, key=init_move_vals.get)
    # print("best move", best_move)
    # print("best move", decode(best_move))
    moveList.append(decode(best_move))
    # print("best val", init_move_vals[best_move])


    # print("*****", moveList[0])
  

    return init_move_vals[best_move], moveList, moveTree

#     # how to save original depth
#     # orig_depth = depth
#     if depth == 0 :
#         return evaluate(board), [], {}

#     # initial_move
#     # if condition for initial move
#     if depth == 1 :
#       vals_for_initial = []
#       initial_moves = [ move for move in generateMoves(side, board, flags) ] #generate list of possible moves

#       # if original_depth == curr_depth :
#       for move in initial_moves :
#         new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
#         value = evaluate(new_board)

#       vals_for_initial.append(value)
  
#     # if orig_depth == depth :
#     #   for move in moves :
#     #     new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
#     #     val_result_of_stochastic, moveList, moveTree_inner = stochastic(new_side, new_board, new_flags, 1, 0, None)
    
#     # rest of moves
#     # else :

#     for initial_move in initial_moves :
#       moves = [ move for move in generateMoves(side, board, flags) ] #generate list of possible moves
#       for moves in moves :
#         val_result_of_stochastic, moveList, moveTree_inner = stochastic(new_side, new_board, new_flags, depth - 1, breadth, chooser)

#     each_val_path = 0
#     if side == False :#player0(white)
#       value = -sys.maxsize
#       for move in moves:
#         new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
#         val_result_of_stochastic, moveList, moveTree_inner = stochastic(new_side, new_board, new_flags, depth - 1, breadth, chooser)

#         each_val_path += val_result_of_stochastic
    
#       average_path_val = each_val_path / depth

#       if average_path_val > value :
#         value = average_path_val

#       else :#player1(black)
#         return None, None, None

# # def stochastic_helper(side, board, flags):
# #   vals_for_initial = []
# #   moves = [ move for move in generateMoves(side, board, flags) ] #generate list of possible moves

# #   # if original_depth == curr_depth :
# #   for move in moves :
# #     new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
# #     value = evaluate(new_board)

# #     vals_for_initial.append(value)
# #       # val_result_of_stochastic, moveList, moveTree_inner = stochastic_helper(side, board, flags, curr_depth, breadth, chooser, original_depth)
  
# #   return vals_for_initial, moves

# def stochastic_recurse_helper(side, board, flags, depth, breadth, chooser, initial_move):
#   result_moveList = []
#   total_path_value = 0
#   if depth == 0 :
#     return evaluate(board), [], {}
  
#   moves = [ move for move in generateMoves(side, board, flags) ] #generate list of possible moves
#   if side == False : #player0(white)
#     moveTree = {}

#     for move in moves :
#       new_side, new_board, new_flags = makeMove(side, board, move[0], move[1], flags, move[2])
#       indiv_value, moveList, moveTree_inner = stochastic_recurse_helper(new_side, new_board, new_flags, depth - 1, breadth, chooser, initial_move)

#     moveTree[encode(*move)] = moveTree_inner

#     # somehow sum values for one path and get average

#   else: #player1(black)

#   return val_for_each_path, result_moveList, moveTree
