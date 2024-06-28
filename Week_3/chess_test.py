import chess
# import chess.pgn
# import copy



# # Open the PGN file
# with open("pgn_data.pgn") as pgn_file:
#     # Read the first game in the file
#     game = chess.pgn.read_game(pgn_file)
    
#     # Initialize a board from the starting position
#     board = game.board()
    
#     # Iterate through all the moves in the game
#     for move in game.mainline_moves():
#         board.push(move)
    
#     # Print the final position of the board


board=chess.Board()
# for i in str(board):
#     print(i)

# history=[""]

# tempboard = chess.Board()
#         for i in range(len(history)):
#             tempboard.push_san(history[i])
#         print(tempboard)





# print(type(board))

print(len(list((board.legal_moves))))

# while(True):
#     move=input("Move: ")
#     if move=="quit":
#         break
#     board.push_san(move)
#     print(board)
    
# new_board=copy.deepcopy(board)
# move=input("next move")
# if move!="q":
#     new_board.push_san(move)
# print(board)
# print(new_board)

# print(board.legal_moves)
# print(board.legal_moves())
for legal_move in board.legal_moves:
    # board.push_san(legal_move)
    move_uci=legal_move
    reqmove = chess.Move.from_uci(str(move_uci))
    move_san=board.san(reqmove)
    print(move_san)
    board.push_san(move_san)
    print(board)
    break
#     board.push(chess.Move.from_uci(str(legal_move)))
#     print(str(board))
#     break

# for square in chess.SQUARES:
#     print(square)