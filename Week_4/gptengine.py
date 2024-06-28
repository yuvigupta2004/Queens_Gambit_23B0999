import copy
import math
import logging
import chess

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

board_positions_val_dict = {}
visited_histories_list = []

help = 0

def sgn(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

class ChessBoard:
    def __init__(self, board=None):
        if board is not None:
            self.board = board
        else:
            self.board = chess.Board()

    def current_player(self):
        return 1 if self.board.turn == chess.WHITE else 2

    def get_board(self):
        return self.board

    def is_win(self):
        if self.board.is_checkmate():
            return 3 - self.current_player()
        return False

    def is_draw(self):
        return self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.can_claim_draw()

    def get_valid_actions(self):
        valid_actions = []
        good_moves = ["+", "#", "Q"]
        for legal_move in self.board.legal_moves:
            move_san = self.board.san(legal_move)
            if str(move_san)[-1] in good_moves or str(move_san)[1] == 'x':
                valid_actions.insert(0, move_san)
            else:
                valid_actions.append(move_san)
        return valid_actions

    def is_terminal_history(self):
        return self.is_win() or self.is_draw()

    def get_utility_given_terminal_history(self):
        if self.is_draw():
            return 0
        if self.is_win() == 1:
            return 10**10
        if self.is_win() == 2:
            return -10**10

    def update_history(self, action):
        new_board = copy.deepcopy(self.board)
        new_board.push_san(action)
        return ChessBoard(board=new_board)

    def get_board_str(self):
        return str(self.board)

    def StaticValue(self):
        value = (sgn(self.PieceDifference())) * (2 ** abs(self.PieceDifference()))
        current_player = self.current_player()
        if current_player == 1:
            value += len(list(self.board.legal_moves)) / 50
        else:
            value -= len(list(self.board.legal_moves)) / 50
        return value

    def PieceDifference(self):
        PIECE_VALUES = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }
        white_score = 0
        black_score = 0
        for square in chess.SQUARES:
            rownumber = 1 + int(square / 8)
            columnnumber = 1 + square % 8
            squareutility = (8 - abs(rownumber - 4.5) - abs(columnnumber - 4.5)) / 40
            piece = self.board.piece_at(square)
            if piece:
                value = PIECE_VALUES.get(piece.piece_type, 0)
                if piece.color == chess.WHITE:
                    white_score += squareutility * value
                else:
                    black_score += squareutility * value
        return white_score - black_score

temp = 1000

def alpha_beta_pruning(history_obj, alpha, beta, depth, max_player_flag):
    global visited_histories_list
    visited_histories_list.append(str(history_obj))
    logging.debug(f"Evaluating board:\n{history_obj.board}")
    
    global help, temp
    help += 1

    if history_obj.is_win():
        return history_obj.get_utility_given_terminal_history()

    if depth == 0:
        return history_obj.StaticValue()

    if max_player_flag:
        maxEval = -math.inf
        for action in history_obj.get_valid_actions():
            child = history_obj.update_history(action)
            child_str = str(child)
            if child_str in board_positions_val_dict:
                eval = board_positions_val_dict[child_str]
            else:
                eval = alpha_beta_pruning(child, alpha, beta, depth - 1, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        board_positions_val_dict[history_obj.get_board_str()] = maxEval
        return maxEval
    else:
        minEval = math.inf
        for action in history_obj.get_valid_actions():
            child = history_obj.update_history(action)
            child_str = child.get_board_str()
            if child_str in board_positions_val_dict:
                eval = board_positions_val_dict[child_str]
            else:
                eval = alpha_beta_pruning(child, alpha, beta, depth - 1, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        board_positions_val_dict[history_obj.get_board_str()] = minEval
        return minEval

def solve_alpha_beta_pruning(history_obj, alpha, beta, depth, max_player_flag):
    global visited_histories_list
    val = alpha_beta_pruning(history_obj, alpha, beta, depth, max_player_flag)
    return val, visited_histories_list

if __name__ == "__main__":
    tscno = input("Enter Testcase Number: ")
    tscno = tscno + ".txt"

    with open(tscno, "r") as f:
        fen = f.read()

    matein3 = chess.Board()
    matein3.set_fen(fen)
    logging.info(f"Starting board:\n{matein3}")
    fen_fields = fen.split()
    active_color = fen_fields[1]
    maxflag = active_color == 'w'
    
    logging.info("Start alpha-beta pruning")
    value, visited_histories = solve_alpha_beta_pruning(ChessBoard(board=matein3), -math.inf, math.inf, 15, maxflag)
    logging.info(f"Maxmin value: {value}")
    logging.info(f"Number of histories visited: {len(visited_histories)}")
    logging.info("End")
