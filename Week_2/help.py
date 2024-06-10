import copy  # use it for deepcopy if needed
import math
import logging
import time

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

# Global variable to keep track of visited board positions. This is a dictionary with keys as self.boards as str and
# value represents the maxmin value. Use the get_boards_str function in History class to get the key corresponding to
# self.boards.
board_positions_val_dict = {}
# Global variable to store the visited histories in the process of alpha beta pruning.
visited_histories_list = []

class History:
    def __init__(self, num_boards=2, history=None):
        self.num_boards = num_boards
        self.history = history if history is not None else []
        self.boards = [['0'] * 9 for _ in range(num_boards)]  # Initialize boards with '0'
        self.player = 1  # Starting player

    def get_valid_actions(self):
        # Returns a list of valid actions (empty positions)
        valid_actions = []
        for board_index in range(self.num_boards):
            for position in range(9):
                if self.boards[board_index][position] == '0':
                    valid_actions.append(board_index * 9 + position)
        return valid_actions

    def update_history(self, action):
        new_history = copy.deepcopy(self)
        board_index = action // 9
        position = action % 9
        new_history.boards[board_index][position] = 'x' if new_history.player == 1 else 'o'
        new_history.history.append(action)
        new_history.player = 3 - new_history.player  # Toggle player between 1 and 2
        return new_history

    def get_boards_str(self):
        return ''.join([''.join(board) for board in self.boards])

def alpha_beta_pruning(history_obj, alpha, beta, max_player_flag):
    global board_positions_val_dict, visited_histories_list
    board_key = history_obj.get_boards_str()

    if board_key in board_positions_val_dict:
        return board_positions_val_dict[board_key]

    visited_histories_list.append(history_obj.history)

    if max_player_flag:
        maxEval = -math.inf
        for action in history_obj.get_valid_actions():
            eval = alpha_beta_pruning(history_obj.update_history(action), alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        board_positions_val_dict[board_key] = maxEval
        return maxEval
    else:
        minEval = math.inf
        for action in history_obj.get_valid_actions():
            eval = alpha_beta_pruning(history_obj.update_history(action), alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        board_positions_val_dict[board_key] = minEval
        return minEval

def solve_alpha_beta_pruning(history_obj, alpha, beta, max_player_flag):
    global visited_histories_list
    visited_histories_list.clear()
    val = alpha_beta_pruning(history_obj, alpha, beta, max_player_flag)
    return val, visited_histories_list

if __name__ == "__main__":
    logging.info("start")
    logging.info("alpha beta pruning")
    initial_history = History(num_boards=2)
    value, visited_histories = solve_alpha_beta_pruning(initial_history, -math.inf, math.inf, True)
    logging.info("maxmin value {}".format(value))
    logging.info("Number of histories visited {}".format(len(visited_histories)))
    logging.info("end")
