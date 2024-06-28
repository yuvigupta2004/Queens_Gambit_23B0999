from engine import alpha_beta_pruning
from engine import Chess_Board
import chess
import math
import logging
import json
from tqdm import tqdm

import cProfile
import re

with open('mate_in_2.json', 'r') as file:
    puzzles = json.load(file)

# logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


# Global variable to store the visited histories in the process of alpha beta pruning.
# visited_histories_list = []
# fen="8/5p2/5k1P/3Q1P1P/6PP/4NR2/6P1/5K2 w - - 0 5"

# chessboard=Chess_Board(chess.Board())
# # print(chess.Board(fen))
# fen_fields = fen.split()
# active_color = fen_fields[1]
# if active_color=='w':
#     maxflag=True
# else:
#     maxflag=False
# board=chess.Board()
# # print(board.fen())
# puzzles={"2R4K/R1P1p1p1/1P1B3n/bB3P2/brppP3/nP1p1P1P/k3ppPp/Nq2Q1rN w - - 0 1":"1. e4"}

# print(board.get_board_str())
# logging.info("Start Solving")
total=0
correct=0

logging.info("Start")
for puzzle in tqdm(puzzles):
    # if total==0:
    #     total=1
    #     continue
    # if total>20:
    #     break
    # print(puzzle)
    # print("----------")
    
    total+=1
    # logging.info("solving puzzle no: {}".format(total))
    
    moves=puzzles[puzzle]
    movelist=moves.split()
    # print(movelist[0])
    board=chess.Board(puzzle)
    
    
    chessboard=Chess_Board(board)
    fen_fields = str(board.fen()).split()
    active_color = fen_fields[1]
    
    if active_color=='w':
        maxflag=True
    else:
        maxflag=False
        
    
    
    board_positions_val_dict = {}
    # print(chessboard.board)

    eval,bestmove = alpha_beta_pruning(chessboard,-math.inf,math.inf,3,maxflag,board_positions_val_dict)   
 
    
    
       
    if bestmove!=movelist[1]:
        if (eval!=10**5):
            print(eval)
            print(puzzle)
            print(bestmove)
            print(movelist[1])
        else: 
            correct+=1
    
    else:
        correct+=1
   
    
logging.info("Total: {} | Correct: {}".format(total,correct))
# cProfile.run('re.compile("foo|bar")')   

# logging.info("End")