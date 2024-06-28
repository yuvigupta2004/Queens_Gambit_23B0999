import math
import logging
import chess
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
    
    
    
    # valid_actions=[]
    # goodmoves=set{"+","Q"}
    
    # for move in board.legal_moves:
    #     sanmove=board.san(move)
    #     movestr_final=str(sanmove)[-1]
    #     if movestr_final == '#':
    #         return [sanmove]
    #     if movestr_final in goodmoves:
    #         valid_actions.insert(0,sanmove)
    #     elif str(sanmove)[1] == 'x':
    #         valid_actions.insert(0,sanmove)
    #     else:
    #         valid_actions.append(sanmove)
    
    # return valid_actions
    


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
    piecediff=PieceDifference(board)
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
    
    # boardstr=history_obj.get_board_str()
    
    if is_terminal_history(history_obj):
        return get_utility_given_terminal_history(history_obj), None
    if depth==0:
        return StaticValue(history_obj), None 
    
    # if boardstr in board_positions_val_dict:
    #     return board_positions_val_dict[boardstr]
        
    bestmove=""   
    
    if max_player_flag:
        maxEval = -math.inf
        for action in get_valid_actions(history_obj):    
            child=update_history(history_obj,action)
            # childstr=child.get_board_str()  
            
            # if childstr in board_positions_val_dict:
            #     eval,abcd = board_positions_val_dict[childstr]  
            # if True:
            #     if ((str(action)[1] == 'x')):
            #         eval,abcd = alpha_beta_pruning(child,alpha,beta,depth-1,False)
            #     else:
            #         eval,abcd = alpha_beta_pruning(child,alpha,beta,depth-1,False)
            
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
            # childstr=child.get_board_str()
            
            # if childstr in board_positions_val_dict:
            #     eval,abcd = board_positions_val_dict[childstr]
            # if True:    
            #     if ((str(action)[1] == 'x')) :
            #         eval,abcd = alpha_beta_pruning(child,alpha,beta,depth-1,True)
            #     else:
            #         eval,abcd = alpha_beta_pruning(child,alpha,beta,depth-1,True)
            
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
    





def solve_alpha_beta_pruning(history_obj, alpha, beta, depth, max_player_flag):
    global visited_histories_list
    # board_positions_val_dict={}
    val,bestmove = alpha_beta_pruning(history_obj, alpha, beta, depth, max_player_flag)
    return val, visited_histories_list, bestmove


if __name__ == "__main__":
    # tscno=input("Enter Testcase Number: ")
    for tscno in range(10):
        
        tscno=str(tscno)
        tscno=tscno+".txt"
        
        with open(tscno,"r") as f:
            fen=f.read()
        # Create a new board object
        matein3 = chess.Board()
        # Set the board to the position defined by the FEN string
        matein3.set_fen(fen)
        # print(matein3)
        fen_fields = fen.split()
        active_color = fen_fields[1]
        if active_color=='w':
            maxflag=True
        else:
            maxflag=False
        # print(maxflag)
        # logging.info("start")
        # logging.info("alpha beta pruning")
        # print(Chess_Board(board=matein3).current_player())
        
        value, visited_histories, bestmove = solve_alpha_beta_pruning(Chess_Board(board=matein3), -math.inf, math.inf, 6, maxflag)
        
        print(maxflag, value, bestmove)
        # if (2*int(maxflag)-1)*int(value) == 1000 :
        #     print("Testcase {} Passed".format(tscno))
            
        # else:
        #     print("Testcase {} Failed".format(tscno))
        # print("maxmin value {}".format(value))
        

    # logging.info("Number of histories visited {}".format(len(visited_histories)))
    # # logging.info("maxmin memory")
    # # logging.info("maxmin value {}".format(maxmin(History(history=[], num_boards=2), True)))
    # logging.info("end")
