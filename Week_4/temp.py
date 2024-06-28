import chess

# Create a chess board
board = chess.Board()

# Get all legal moves
legal_moves = board.legal_moves

# Convert moves to standard algebraic notation
standard_notation_moves = [board.san(move) for move in legal_moves]

# Print the moves
for move in standard_notation_moves:
    print(move)