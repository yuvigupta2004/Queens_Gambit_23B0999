import math
import logging
import chess
import numpy as np
logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


def sgn(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
    

def current_player(board):
    
    if board.turn==chess.WHITE:
        return 1
    else:
        return 2



def is_win(board):

    currentplayer=current_player(board)
    if board.is_checkmate():
        return 3-currentplayer
    return False


def is_draw(board):
    if board.is_stalemate():
        return True
    if board.is_insufficient_material():
        return True
    return False
    

def get_valid_actions(board):
    
    good_moves = []
    capture_moves = []
    other_moves = []
    
    
    
    for move in board.legal_moves:
        sanmove = board.san(move)
        if sanmove[-1]=='#':
            return [sanmove]
        if sanmove[-1] in {'+', 'Q'}:
            good_moves.append(sanmove)
        elif sanmove[1] == 'x':
            capture_moves.append(sanmove)
        else:
            other_moves.append(sanmove)
    
    # Combine all the categorized moves
    valid_actions = good_moves + capture_moves + other_moves
    return valid_actions
    
    
    
    
    # legal_moves=board.legal_moves
    # move_value_dict={}
    
    # for move in legal_moves: 
    #     board.push(move)
    #     sanmove=board.san(move)
    #     if board.is_checkmate():
    #         board.pop()
    #         return [sanmove]
    #     move_value_dict[sanmove]=len(list(board.legal_moves))
    #     if board.is_check():
    #         move_value_dict[sanmove] = -10*3
    #     board.pop()
    # return sorted(move_value_dict, key=lambda x: move_value_dict[x])
    
    # legal_moves=board.legal_moves
    # move_value_dict={}
    # standard_notation_moves = [board.san(move) for move in legal_moves]
    # for sanmove in standard_notation_moves: 
    #     board.push_san(sanmove)
    #     if board.is_checkmate():
    #         board.pop()
    #         return [sanmove]
    #     move_value_dict[sanmove]=len(list(board.legal_moves))
    #     if board.is_check():
    #         move_value_dict[sanmove] = -10*3
    #     board.pop()
    # return sorted(move_value_dict, key=lambda x: move_value_dict[x])
    
    
    
    
    
    
    


def is_terminal_history(board):
    
    if is_win(board) | is_draw(board) :
        return True
    # Feel free to implement this in anyway if needed
    return False
    pass

def get_utility_given_terminal_history(board):
    # Feel free to implement this in anyway if needed
    wincheck=is_win(board)
    
    if wincheck:
        return 10**5 * (3-2*wincheck)
    
    return 0
    pass

def update_history(board, action):
    # In case you need to create a deepcopy and update the history obj to get the next history object.
    
    new_board=board.copy()
    new_board.push_san(action)
    return new_board
    # Feel free to implement this in anyway if needed
    pass


def get_board_str(board):
    return str(board)

def StaticValue(board):

    value=0
    piecediff=PieceDifference(board)/100
    value=value+(sgn(piecediff))*(2**abs(piecediff))
    return value

def PieceDifference(board):
    PIECE_VALUES = {
    "p": 1,
    "n": 3,
    "b": 3.2,
    "r": 5,
    "q": 9
    }
    
    white_points = 0
    black_points = 0

    for i in board.fen().split()[0]:
        
        value =  PIECE_VALUES.get(i.lower(), 0)
        
        if i.isupper():
            white_points += value
        else:
            black_points += value
    
    return round(white_points - black_points,5)
    
    




def alpha_beta_pruning(history_obj, alpha, beta, depth, max_player_flag):
    
    # boardstr=history_obj.fen().split()[0] 
    
    if is_terminal_history(history_obj):
        return get_utility_given_terminal_history(history_obj), None
    if depth==0:
        return 0, None 
    
    # if boardstr in board_positions_val_dict:
    #     return board_positions_val_dict[boardstr]
        
    bestmove=""   
    
    if max_player_flag:
        maxEval = -math.inf
        for action in get_valid_actions(history_obj):    
            child=update_history(history_obj,action)
            
            
            # childstr=child.fen().split()[0] 
            
            # if childstr in board_positions_val_dict:
            #     eval,abcd = board_positions_val_dict[childstr]  
            # else:
            #     if ((str(action)[1] == 'x')):
            #         eval,abcd = alpha_beta_pruning(child,alpha,beta,depth-1,False,board_positions_val_dict)
            #     else:
            #         eval,abcd = alpha_beta_pruning(child,alpha,beta,depth-1,False,board_positions_val_dict)
            
            eval,abcd = alpha_beta_pruning(child,alpha,beta,depth-1,False)
                       
            if eval > maxEval:
                bestmove=str(action) 
                           
            maxEval = max(maxEval, eval)
            alpha = max(alpha,eval)
            
            if beta <= alpha:
                break
            
        # board_positions_val_dict[boardstr]=maxEval,bestmove
        return maxEval,bestmove
    
    else:
        minEval = math.inf
        for action in get_valid_actions(history_obj):
            child=update_history(history_obj,action)
            
            # childstr=child.fen().split()[0] 
            
            # if childstr in board_positions_val_dict:
            #     eval,abcd = board_positions_val_dict[childstr]
            # else:    
            #     if ((str(action)[1] == 'x')) :
            #         eval,abcd = alpha_beta_pruning(child,alpha,beta,depth-1,True,board_positions_val_dict)
            #     else:
            #         eval,abcd = alpha_beta_pruning(child,alpha,beta,depth-1,True,board_positions_val_dict)
            
            eval,abcd = alpha_beta_pruning(child,alpha,beta,depth-1,True)

            if eval < minEval:
                bestmove=str(action)
            
            minEval = min(minEval, eval)
            
            beta = min(beta,eval)
            if beta <= alpha:
                break
        # board_positions_val_dict[boardstr]=minEval,bestmove
        return minEval,bestmove
        
    
    return -2
    







