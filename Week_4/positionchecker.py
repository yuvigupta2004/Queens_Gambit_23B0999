from ihatebajaj import alpha_beta_pruning
import chess
import logging
import time

logging.info("Start")
start=time.time()

puzzle=input("Enter Position Fen")
depth=int(input("Enter Depth"))
board=chess.Board(puzzle)

fen_fields = puzzle.split()
active_color = fen_fields[1]

if active_color=='w':
    maxflag=True
else:
    maxflag=False
        
eval,bestmove = alpha_beta_pruning(board,-1*10**3,10**3,depth,maxflag)   
    
print("Total time:",time.time()-start)
logging.info("End")