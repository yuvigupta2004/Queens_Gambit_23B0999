#include <iostream>
#include <vector>
#include <cmath>
#include <bits/stdc++.h>
#include <map>
#include "chess.hpp" 

using namespace std;
using namespace chess;

// Helper function to get the sign of a number
int sgn(double x) {
    if (x > 0) return 1;
    if (x < 0) return -1;
    return 0;
}

// Get current player
int current_player(const Board& board) {
    return board.sideToMove() == Color::WHITE ? 1 : 2;
}

// Check if the current board position is a win for any player
int is_win(const Board& board) {
    pair<GameResultReason, GameResult> result = board.isGameOver();
    int currentPlayer = current_player(board);
    if (result.second == GameResult::WIN || result.second == GameResult::LOSE) {
        return 3 - currentPlayer;
    }
    return false;
}

// Check if the current board position is a draw
bool is_draw(const Board& board) {
    pair<GameResultReason, GameResult> result = board.isGameOver();
    if (result.second == GameResult::DRAW){
        return true;
    }
    return false;
    
}

// Get all valid actions (moves) for the current board position
vector<Move> get_valid_actions(const Board& board) {
    vector<Move> good_moves;
    vector<Move> capture_moves;
    vector<Move> other_moves;


    Movelist moves;
    movegen::legalmoves(moves, board);

    for (const auto &move : moves) {
        string san_move = uci::moveToSan(board, move);
        if (san_move.back() == '#') {
            return {move};
        }
        if (san_move.back() == '+' || san_move.back() == 'Q') {
            good_moves.push_back(move);
        } 
        else if (san_move[1] == 'x') {
            capture_moves.push_back(move);
        } 
        else {
            other_moves.push_back(move);
        }
    }

    vector<Move> valid_actions;
    valid_actions.insert(valid_actions.end(), good_moves.begin(), good_moves.end());
    valid_actions.insert(valid_actions.end(), capture_moves.begin(), capture_moves.end());
    valid_actions.insert(valid_actions.end(), other_moves.begin(), other_moves.end());
    return valid_actions;
}

// Check if the game has reached a terminal state (win or draw)
bool is_terminal_history(const Board& board) {
    return (board.isGameOver().second != GameResult::NONE);
}

// Get utility value for terminal board states
long long int get_utility_given_terminal_history(const Board& board) {
    int win_check = is_win(board);
    if (win_check) {
        return pow(10, 5) * (3 - 2 * win_check);
    }
    return 0;
}

// Update board history with a new move
Board update_history(const Board& board, const Move& action) {
    Board new_board = board;
    new_board.makeMove(action);
    return new_board;
}

// // Get board representation as a string
// string get_board_str(const Board& board) {
//     return board.to_string();
// }

// Calculate piece difference for a board position
double PieceDifference(const Board& board) {
    map<Piece, double> PIECE_VALUES {
        {Piece::WHITEPAWN, 1},
        {Piece::WHITEKNIGHT, 2.9},
        {Piece::WHITEBISHOP, 3.2},
        {Piece::WHITEROOK, 5},
        {Piece::WHITEQUEEN, 9.75},
        {Piece::BLACKPAWN, 1},
        {Piece::BLACKKNIGHT, 2.9},
        {Piece::BLACKBISHOP, 3.2},
        {Piece::BLACKROOK, 5},
        {Piece::BLACKQUEEN, 9.75}
    };

    map<Piece, array<int, 64>> SQUARE_PIECE_VALUES {
    {Piece::WHITEPAWN, {
        0,   0,   0,   0,   0,   0,   0,   0,
        20,  50,  40,  20,  20,  40,  50,  20,
        30,  10,  20,  25,  25,  20,  10,  30,
        5,   5,   10,  40,  40,  10,  5,   5,
        0,   0,   0,   20,  20,  0,   0,   0,
        5,   5,   10,  0,   0,   10,  5,   5,
        50,  50,  50,  50,  50,  50,  50,  50,
        0,   0,   0,   0,   0,   0,   0,   0
    }},
    {Piece::WHITEKNIGHT, {
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0,   0,   0,   0,   -20, -40,
        -30, 0,   20,  15,  15,  20,  0,   -30,
        -30, 5,   15,  20,  20,  15,  5,   -30,
        -30, 5,   15,  20,  20,  15,  5,   -30,
        -30, 5,   10,  15,  15,  10,  5,   -30,
        -40, -20, 10,  5,   5,   10,  -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    }},
    {Piece::WHITEBISHOP, {
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10,  10,  0,   0,   0,   0,   10,  -10,
        -10,  10,  10,  10,  10,  10,  10,  -10,
        -10,  0,   10,  10,  10,  10,  0,   -10,
        -10,  10,  5,   10,  10,  5,   10,  -10,
        -10,  0,   5,   10,  10,  5,   0,   -10,
        -10,  0,   0,   0,   0,   0,   0,   -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    }},
    {Piece::WHITEROOK, {
        0,   0,   15,  15,  15,  15,  0,   0,
        -5,  0,   0,   0,   0,   0,   0,   -5,
        -5,  0,   0,   0,   0,   0,   0,   -5,
        -5,  0,   0,   0,   0,   0,   0,   -5,
        -5,  0,   0,   0,   0,   0,   0,   -5,
        -5,  0,   0,   0,   0,   0,   0,   -5,
        5,   10,  10,  10,  10,  10,  10,  5,
        5,   5,   5,   5,   5,   5,   5,   5
    }},
    {Piece::WHITEQUEEN, {
        -20, -10, -10, -5,  -5,  -10, -10, -20,
        -10,  0,   0,   0,   0,   0,   0,   -10,
        -10,  0,   5,   5,   5,   5,   0,   -10,
        -5,   0,   5,   5,   5,   5,   0,   -5,
        0,    0,   5,   5,   5,   5,   0,   0,
        -10,  0,   5,   5,   5,   5,   0,   -10,
        -10,  0,   0,   0,   0,   0,   0,   -10,
        -20, -10, -10, -5,  -5,  -10, -10, -20
    }},
    // Black pieces (mirrored vertically)
    {Piece::BLACKPAWN, {
        0,   0,   0,   0,   0,   0,   0,   0,
        50,  50,  50,  50,  50,  50,  50,  50,
        5,   5,   10,  0,   0,   10,  5,   5,
        0,   0,   0,   20,  20,  0,   0,   0,  
        5,   5,   10,  40,  40,  10,  5,   5,
        30,  10,  20,  25,  25,  20,  10,  30,
        20,  50,  40,  20,  20,  40,  50,  20,
        0,   0,   0,   0,   0,   0,   0,   0
    }},
    {Piece::BLACKKNIGHT, {
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 10,  5,   5,   10,  -20, -40,
        -30, 5,   10,  15,  15,  10,  5,   -30,
        -30, 5,   15,  20,  20,  15,  5,   -30,
        -30, 5,   15,  20,  20,  15,  5,   -30,
        -30, 0,   20,  15,  15,  20,  0,   -30,
        -40, -20, 0,   0,   0,   0,   -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    }},
    {Piece::BLACKBISHOP, {
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10,  0,   0,   0,   0,   0,   0,   -10,
        -10,  0,   5,   5,   5,   5,   0,   -10,
        -10,  5,   10,  10,  10,  10,  5,   -10,
        -10,  0,   10,  10,  10,  10,  0,   -10,
        -10,  10,  10,  10,  10,  10,  10,  -10,
        -10,  10,  0,   0,   0,   0,   10,  -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    }},
    {Piece::BLACKROOK, {
        5,   10,  10,  10,  10,  10,  10,  5,
        5,   5,   5,   5,   5,   5,   5,   5,
        -5,  0,   0,   0,   0,   0,   0,   -5,
        -5,  0,   0,   0,   0,   0,   0,   -5,
        -5,  0,   0,   0,   0,   0,   0,   -5,
        -5,  0,   0,   0,   0,   0,   0,   -5,
        0,   0,   15,  15,  15,  15,  0,   0,
        0,   0,   0,   0,   0,   0,   0,   0
    }},
    {Piece::BLACKQUEEN, {
        -20, -10, -10, -5,  -5,  -10, -10, -20,
        -10,  0,   5,   5,   5,   5,   0,   -10,
        -10,  0,   5,   5,   5,   5,   0,   -10,
        -5,   0,   5,   5,   5,   5,   0,   -5,
        0,    0,   5,   5,   5,   5,   0,   0,
        -10,  0,   0,   0,   0,   0,   0,   -10,
        -10,  0,   0,   0,   0,   0,   0,   -10,
        -20, -10, -10, -5,  -5,  -10, -10, -20
    }}
    
    };

    double white_points = 0;
    double black_points = 0;

    for (int i=0; i<64; i++){

        int rownumber = 1 + i%8;
        int columnnumber = 1 + i/8;

        int squarenumber = (rownumber-1)* 8 + (columnnumber-1);

        Square squarecheck = Square(i);
        Piece piece = board.at(squarecheck);

        if (piece == Piece::NONE || piece == Piece::BLACKKING || piece == Piece::WHITEKING){
            continue;
        }

        double piecevalue = PIECE_VALUES[piece];
        
        Color piececolor = piece.color();

        double pieceatsquarevalue = SQUARE_PIECE_VALUES[piece][squarenumber];


        if (piececolor == Color::WHITE){
            double value=piecevalue*(1+pieceatsquarevalue/200);
            white_points += value;
        }
        else{
            double value=piecevalue*(1+pieceatsquarevalue/200);
            black_points += value;
        }
    
    } 


    if ((white_points - black_points)<=pow(10,-3)){
        return 0;
    }  
    else{
        return white_points - black_points;
    }

}


// Calculate static value for a board position
double StaticValue(const Board& board) {
    double value = 0;
    double piece_diff = PieceDifference(board) / 5;
    // cout<<"No Error in PieceDifference: "<<piece_diff<<endl;
    // value += sgn(piece_diff) * pow(2, abs(piece_diff));
    return piece_diff;
}


// Alpha-beta pruning algorithm for move evaluation
pair<double, Move> alpha_beta_pruning(const Board& board, double alpha, double beta, int depth, bool max_player_flag) {
    if (is_terminal_history(board)) {
        // cout<<"Entered This"<<endl;
        // cout<<board<<endl;
        return {get_utility_given_terminal_history(board), Move()};
    }
    if (depth == 0) {
        // cout<<"Entered Depth 0"<<endl;
        // cout<<board<<endl;
        return {StaticValue(board), Move()};
    }

    Move best_move;
    int firstmovecheck = 1;
    
//bye kunal
    if (max_player_flag) {
        double max_eval = -numeric_limits<int>::infinity();
        for (const Move& action : get_valid_actions(board)) {
            if (firstmovecheck==1){
                best_move = action;
                firstmovecheck=0;
            }
            Board child = update_history(board, action);
            // cout<<"---------------------------------"<<endl;
            // cout<<"Parent Move: "<<action<<endl;
            double eval = alpha_beta_pruning(child, alpha, beta, depth - 1, false).first;
            // cout<<"Parent Evaluation: "<<eval<<"   "<<"Move is: "<<action<<endl;
            if (eval > max_eval) {
                // cout<<"Best Move yet is: "<<endl;
                // cout<<"Best Move is: "<<endl;

                best_move = action;
            }
            max_eval = max(max_eval, eval);
            alpha = max(alpha, eval);
            if (beta <= alpha) {
                break;
            }
        }
        // cout<<"-----------------------"<<endl;
        // cout<<"Evaluation is: "<<max_eval<<"    Best Move: "<<best_move<<endl;
        // cout<<"-----------------------"<<endl;
        return {max_eval, best_move};
    } else {
        double min_eval = numeric_limits<int>::infinity();
        for (const Move& action : get_valid_actions(board)) {
            Board child = update_history(board, action);
            if (firstmovecheck==1){
                best_move = action;
                firstmovecheck=0;
            }
            double eval = alpha_beta_pruning(child, alpha, beta, depth - 1, true).first;
            // cout<<"Evaluation: "<<eval<<"   "<<"Move is: "<<action<<endl;
            if (eval < min_eval) {
                best_move = action;
            }
            min_eval = min(min_eval, eval);
            beta = min(beta, eval);
            if (beta <= alpha) {
                break;
            }
        }



        // cout<<"-----------------------"<<endl;
        // cout<<"Evaluation is: "<<min_eval<<"    Best Move: "<<best_move<<endl;
        // cout<<"-----------------------"<<endl;
        return {min_eval, best_move};
    }
    return {-2, Move()};
}



int main(){



    string fen;
    cin>>fen;

    Board board =  Board(fen);

    // cout<<board<<endl;
    // Movelist moves;
    // movegen::legalmoves(moves, board);
    // for (const auto &move : moves) {
    //     Board new_board= update_history(board,move);
    //     cout<<new_board<<endl;
    //     cout<<board<<endl;
    //     string san_move = uci::moveToSan(board, move);
    //     cout<<san_move<<endl;
    //     break;
    // }

    pair<double, Move> plschalja = alpha_beta_pruning(board, -1*pow(10,5), pow(10,5), 5, true);
    // string san_move = uci::moveToSan(board, plschalja.second);
    cout<<"Eval is: "<<plschalja.first<<endl;
    cout<<"Best Move is: "<<plschalja.second<<endl;
}