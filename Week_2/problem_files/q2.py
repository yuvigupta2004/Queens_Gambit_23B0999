import copy  # use it for deepcopy if needed
import math
import logging
import time

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# Global variable to keep track of visited board positions. This is a dictionary with keys as self.boards as str and
# value represents the maxmin value. Use the get_boards_str function in History class to get the key corresponding to
# self.boards.
board_positions_val_dict = {}
# Global variable to store the visited histories in the process of alpha beta pruning.
visited_histories_list = []

help=0

class History:
    def __init__(self, num_boards=2, history=None):
        """
        # self.history : Eg: [0, 4, 2, 5]
            keeps track of sequence of actions played since the beginning of the game.
            Each action is an integer between 0-(9n-1) representing the square in which the move will be played as shown
            below (n=2 is the number of boards).

             Board 1
              ___ ___ ____
             |_0_|_1_|_2_|
             |_3_|_4_|_5_|
             |_6_|_7_|_8_|

             Board 2
              ____ ____ ____
             |_9_|_10_|_11_|
             |_12_|_13_|_14_|
             |_15_|_16_|_17_|

        # self.boards
            empty squares are represented using '0' and occupied squares are 'x'.
            Eg: [['x', '0', 'x', '0', 'x', 'x', '0', '0', '0'], ['0', 0', '0', 0', '0', 0', '0', 0', '0']]
            for two board game

            Board 1
              ___ ___ ____
             |_x_|___|_x_|
             |___|_x_|_x_|
             |___|___|___|

            Board 2
              ___ ___ ____
             |___|___|___|
             |___|___|___|
             |___|___|___|

        # self.player: 1 or 2
            Player whose turn it is at the current history/board

        :param num_boards: Number of boards in the game of Notakto.
        :param history: list keeps track of sequence of actions played since the beginning of the game.
        """
        self.num_boards = num_boards
        if history is not None:
            self.history = history
            self.boards = self.get_boards()
        else:
            self.history = []
            self.boards = []
            for i in range(self.num_boards):
                # empty boards
                self.boards.append(['0', '0', '0', '0', '0', '0', '0', '0', '0'])
        # Maintain a list to keep track of active boards
        self.active_board_stats = self.check_active_boards()
        self.current_player = self.get_current_player()

    def get_boards(self):
        """ Play out the current self.history and get the boards corresponding to the history.

        :return: list of lists
                Eg: [['x', '0', 'x', '0', 'x', 'x', '0', '0', '0'], ['0', 0', '0', 0', '0', 0', '0', 0', '0']]
                for two board game

                Board 1
                  ___ ___ ____
                 |_x_|___|_x_|
                 |___|_x_|_x_|
                 |___|___|___|

                Board 2
                  ___ ___ ____
                 |___|___|___|
                 |___|___|___|
                 |___|___|___|
        """
        boards = []
        # print(self.history,self.num_boards)
        for i in range(self.num_boards):
            boards.append(['0', '0', '0', '0', '0', '0', '0', '0', '0'])
        for i in range(len(self.history)):
            board_num = math.floor(int(self.history[i]) / 9)
            play_position = int(self.history[i]) % 9
            boards[board_num][play_position] = 'x'
        return boards

    def check_active_boards(self):
        """ Return a list to keep track of active boards

        :return: list of int (zeros and ones)
                Eg: [0, 1]
                for two board game

                Board 1
                  ___ ___ ____
                 |_x_|_x_|_x_|
                 |___|_x_|_x_|
                 |___|___|___|

                Board 2
                  ___ ___ ____
                 |___|___|___|
                 |___|___|___|
                 |___|___|___|
        """
        active_board_stat = []
        for i in range(self.num_boards):
            if self.is_board_win(self.boards[i]):
                active_board_stat.append(0)
            else:
                active_board_stat.append(1)
        return active_board_stat

    @staticmethod
    def is_board_win(board):
        for i in range(3):
            if board[3 * i] == board[3 * i + 1] == board[3 * i + 2] != '0':
                return True

            if board[i] == board[i + 3] == board[i + 6] != '0':
                return True

        if board[0] == board[4] == board[8] != '0':
            return True

        if board[2] == board[4] == board[6] != '0':
            return True
        return False

    def get_current_player(self):
        """
        Get player whose turn it is at the current history/board
        :return: 1 or 2
        """
        total_num_moves = len(self.history)
        if total_num_moves % 2 == 0:
            return 1
        else:
            return 2

    def get_boards_str(self):
        boards_str = ""
        for i in range(self.num_boards):
            boards_str = boards_str + ''.join([str(j) for j in self.boards[i]])
        return boards_str

    def is_win(self):
        # Feel free to implement this in anyway if needed
        # print(self.check_active_boards())
        # print(len(set(self.check_active_boards())))
        if ((len(set(self.check_active_boards()))==1) & (self.check_active_boards()[0]==0)):
            return True
        return False
        pass

    def get_valid_actions(self):
        # Feel free to implement this in anyway if needed
        active=self.check_active_boards()
        boards=self.get_boards()
        actions=[]
        for i in range(self.num_boards):
            current_board=boards[i]
            if active[i]:
                for j in range(len(current_board)):
                    if str(current_board[j])==str(0):
                        action=str(9*i+j)
                      
                        actions.append(action)
                        
        
        return actions
        
        pass

    def is_terminal_history(self):
        # Feel free to implement this in anyway if needed
        return self.is_win()
        pass

    def get_value_given_terminal_history(self):
        # Feel free to implement this in anyway if needed
        if self.get_current_player() == 1: 
            return 1
        else: return -1
        pass

    def update_history(self, action):
        # In case you need to create a deepcopy and update the history obj to get the next history object.
        hist=self.history
        new_hist=copy.deepcopy(hist)
        new_hist.append(action)
        return History(self.num_boards,new_hist)
        # Feel free to implement this in anyway if needed
        pass
        
temp=100000

def alpha_beta_pruning(history_obj, alpha, beta, max_player_flag):
    """
        Calculate the maxmin value given a History object using alpha beta pruning. Use the specific move order to
        speedup (more pruning, less memory).

    :param history_obj: History class object
    :param alpha: -math.inf
    :param beta: math.inf
    :param max_player_flag: Bool (True if maximizing player plays)
    :return: float
    """
    # These two already given lines track the visited histories.
    global visited_histories_list
    visited_histories_list.append(history_obj.history)
    
    
    # global help,temp
    # help=help+1
    # if help%100000 == 0:
    #     print(help)
    # print(len(history_obj.get_valid_actions()))
    
    # TODO implement
    # time.sleep(1)
    
    # if len(history_obj.get_valid_actions())==0:
    #     print(history_obj.history)
    #     print(history_obj.get_boards())
    #     print(history_obj.is_win())
    #     time.sleep(100)
    
    
    
    if history_obj.is_win():
        
        # if help>temp:
        #     print("Reached a node")
        #     print(history_obj.history)
        #     temp=temp+100000
        #     print(alpha,beta)
        return 2*int(max_player_flag)-1
    
    
    if max_player_flag:
        maxEval = -math.inf
        
        for action in history_obj.get_valid_actions():
            child=history_obj.update_history(action)
            childstr=child.get_boards_str()
            if childstr in board_positions_val_dict:
                eval = board_positions_val_dict[childstr]
            else:
                eval = alpha_beta_pruning(child,alpha,beta,False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha,eval)
            if beta <= alpha:
                break
        board_positions_val_dict[history_obj.get_boards_str()]=maxEval
        return maxEval
    
    else:
        minEval = math.inf
        for action in history_obj.get_valid_actions():
            child=history_obj.update_history(action)
            childstr=child.get_boards_str()
            if childstr in board_positions_val_dict:
                eval = board_positions_val_dict[childstr]
            else:    
                eval = alpha_beta_pruning(child,alpha,beta,True)
                
            minEval = min(minEval, eval)
            
            beta = min(beta,eval)
            if beta <= alpha:
                break
        board_positions_val_dict[history_obj.get_boards_str()]=minEval
        return minEval
        
    
    return -2
    # TODO implement


# def maxmin(history_obj, max_player_flag):
#     """
#         Calculate the maxmin value given a History object using maxmin rule. Store the value of already visited
#         board positions to speed up, avoiding recursive calls for a different history with the same board position.
#     :param history_obj: History class object
#     :param max_player_flag: True if the player is maximizing player
#     :return: float
#     """
#     # Global variable to keep track of visited board positions. This is a dictionary with keys as str version of
#     # self.boards and value represents the maxmin value. Use the get_boards_str function in History class to get
#     # the key corresponding to self.boards.
#     global board_positions_val_dict
#     # TODO implement
#     return -2
#     # TODO implement


def solve_alpha_beta_pruning(history_obj, alpha, beta, max_player_flag):
    global visited_histories_list
    val = alpha_beta_pruning(history_obj, alpha, beta, max_player_flag)
    return val, visited_histories_list


if __name__ == "__main__":
    logging.info("start")
    logging.info("alpha beta pruning")
    value, visited_histories = solve_alpha_beta_pruning(History(history=[], num_boards=2), -math.inf, math.inf, True)
    logging.info("maxmin value {}".format(value))
    logging.info("Number of histories visited {}".format(len(visited_histories)))
    # logging.info("maxmin memory")
    # logging.info("maxmin value {}".format(maxmin(History(history=[], num_boards=2), True)))
    logging.info("end")
