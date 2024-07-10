#include <iostream>
#include <vector>
#include <cmath>
#include <bits/stdc++.h>
#include <map>
#include "chess.hpp" 
#include <chrono>



using namespace std;
using namespace chess;
using namespace std::chrono;



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


// Check if the game has reached a terminal state (win or draw)
bool is_terminal_history(const Board& board) {
    return (board.isGameOver().second != GameResult::NONE);
}

// Get utility value for terminal board states
double get_utility_given_terminal_history(const Board& board) {
    double win_check = is_win(board);
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


    if (abs(white_points - black_points)<=0.001){
        return 0;
    }  
    else{
        return white_points - black_points;
    }

}


// Calculate static value for a board position
double StaticValue(const Board& board) {
    double piece_diff = PieceDifference(board) / 5;
    // cout<<"No Error in PieceDifference: "<<piece_diff<<endl;
    // value += sgn(piece_diff) * pow(2, abs(piece_diff));
    return piece_diff;
}


// Get all valid actions (moves) for the current board position
vector<Move> get_valid_actions(Board& board) {

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


    
    // std::vector<std::pair<float, Move>> orderedMoveswithvalue;
    // Movelist moves;
    // movegen::legalmoves(moves, board);

    // for (const auto &move : moves) {
    //     board.makeMove(move);
    //     if (board.getHalfMoveDrawType().first == GameResultReason::CHECKMATE) {
    //         board.unmakeMove(move);
    //         return {move};
    //     } 
    //     else {
    //         orderedMoveswithvalue.push_back({StaticValue(board), move});
    //     }
    //     board.unmakeMove(move);
    // }
    // std::sort(orderedMoveswithvalue.begin(), orderedMoveswithvalue.end(), [](const auto& a, const auto& b) {
    //     return a.first > b.first;
    // });
    // std::vector<Move> ordered_moves;
    // for (const auto& move : orderedMoveswithvalue) {
    //     ordered_moves.push_back(move.second);
    // }
    // // for (const auto& move : ordered) {
    // //     std::cout << move << std::endl;
    // // }
    // return ordered_moves;

}








// Alpha-beta pruning algorithm for move evaluation

pair<double, Move> alpha_beta_pruning(Board& board, double alpha, double beta, int depth, bool max_player_flag, map<uint64_t,pair<pair<double,chess::Move>,int>>& StaticMap, int maxtimeinmilli, auto& startTime) {

    uint64_t boardhash= board.hash();
    auto it = StaticMap.find(boardhash);

    if (std::chrono::duration_cast<milliseconds>(std::chrono::high_resolution_clock::now() - startTime).count() >= maxtimeinmilli){
        return {it->second.first};
    }

    

    if (it != StaticMap.end()) {
        if (it->second.second > depth){
        return {it->second.first};
        }
    } 


    if (is_terminal_history(board)) {
        double termeval = get_utility_given_terminal_history(board);
        
        pair<double, Move> ans = {termeval,Move()};

        StaticMap[boardhash] = {ans,depth};

        return ans;
    }

    if (depth == 0) { 

        double ans = StaticValue(board);
        pair<double, Move> termdepthans = {ans,Move()};
        StaticMap[boardhash].first = termdepthans;
        return termdepthans;
    }
    

    Move best_move;
    int firstmovecheck = 1;
    if (max_player_flag) {
        double max_eval = -1000000;
        for (const Move& action : get_valid_actions(board)) {


            if (std::chrono::duration_cast<milliseconds>(std::chrono::high_resolution_clock::now() - startTime).count() >= maxtimeinmilli){
                return {it->second.first};
            }

            if (firstmovecheck==1){
                best_move = action;
                firstmovecheck=0;
            }

            Board child = update_history(board, action);
            uint64_t childhash = child.hash();
            auto childit = StaticMap.find(childhash);

            if (it != StaticMap.end()) {
                if (it->second.second > depth){
                    return it->second.first;
                }

            } 

            pair<GameResultReason, GameResult> result = child.isGameOver();
            if (result.first == GameResultReason::THREEFOLD_REPETITION){
                continue;
            }

            double eval = alpha_beta_pruning(child, alpha, beta, depth - 1, false,StaticMap, maxtimeinmilli, startTime).first;
            if (eval > max_eval) {
                best_move = action;
            }
            max_eval = max(max_eval, eval);
            alpha = max(alpha, eval);
            if (beta <= alpha) {
                break;
            }
        }

        StaticMap[boardhash] = {{max_eval, best_move},depth};
        return {max_eval, best_move};

    } 
    else {
        double min_eval = 1000000;
        for (const Move& action : get_valid_actions(board)) {

            if (std::chrono::duration_cast<milliseconds>(std::chrono::high_resolution_clock::now() - startTime).count() >= maxtimeinmilli){
                return {it->second.first};
            }





            Board child = update_history(board, action);








            uint64_t childhash = child.hash();
            auto childit = StaticMap.find(childhash);

            if (it != StaticMap.end()) {
                if (it->second.second > depth){
                    return it->second.first;
                }

            }

            pair<GameResultReason, GameResult> result = child.isGameOver();
            if (result.first == GameResultReason::THREEFOLD_REPETITION){
                continue;
            }

            if (firstmovecheck==1){
                best_move = action;
                firstmovecheck=0;
            }
            double eval = alpha_beta_pruning(child, alpha, beta, depth - 1, true,StaticMap, maxtimeinmilli, startTime).first;
            if (eval < min_eval) {
                best_move = action;
            }
            min_eval = min(min_eval, eval);
            beta = min(beta, eval);
            if (beta <= alpha) {
                break;
            }
        }

        StaticMap[boardhash] = {{min_eval, best_move},depth};
        return {min_eval, best_move};
    }
    return {-2, Move()};
}





map<uint64_t,pair<pair<double,chess::Move>,int>> StaticMap;
Board globalboard;


void sendResponse(const std::string& response) {
    std::cout << response << std::endl;
}

void handleUci() {
    sendResponse("id name YuvrajEngine_v1");
    sendResponse("id author yuvigupta");
    sendResponse("uciok");
}

void handleIsReady() {
    sendResponse("readyok");
}




void setupInitialPosition() {
    // Set up the initial position on the board
    globalboard = Board();
    StaticMap.clear();
    
    // This function should initialize the board to the starting position
}

void setupPositionFromFEN(const std::string& fen) {
    // Set up the board according to the given FEN string
    globalboard = Board(fen);
    // This function should parse the FEN string and set up the board accordingly
}

void makemove(const std::string& move) {
    // Make a move on the board
    Move Move_move = uci::uciToMove(globalboard, move);
    globalboard.makeMove(Move_move);
    // This function should convert the move string to your engine's move format and apply it
}

void handlePosition(const std::string& positionCommand) {
    std::istringstream iss(positionCommand);
    std::string token;
    iss >> token; // "position"

    std::string positionType;
    iss >> positionType;

    if (positionType == "startpos") {
        // Set up initial position
        setupInitialPosition();
        iss >> token; // Check if there are more tokens, should be "moves" or end of string
    } else if (positionType == "fen") {
        // Read FEN string
        std::string fen;
        while (iss >> token && token != "moves") {
            fen += token + " ";
        }
        setupPositionFromFEN(fen);
    }

    // Handle moves if present
    if (token == "moves") {
        std::string move;
        while (iss >> move) {
            makemove(move);
        }
    }
}

void handleGo(int maxtimeinmilli=10000) {
    // Make the engine start thinking and find the best move
    int initialDepth = 1;
    int maxDepth = 16;
    int depth = initialDepth;

    


    cout<<"-------------------------------------------"<<endl;

    auto startTime = std::chrono::high_resolution_clock::now();
    pair<double, Move> bestMove;
    bool whitemove;
    if (current_player(globalboard)==1){whitemove=true;}
    else{whitemove=false;}
    // Perform iterative deepening with time constraint
    for (depth = initialDepth; depth <= maxDepth; ++depth) {
        bestMove = alpha_beta_pruning(globalboard, -1e5, 1e5, depth, whitemove, StaticMap, maxtimeinmilli, startTime);
        
        // cout<<"Reached Depth: "<<depth<<endl;
        auto NowTime = std::chrono::high_resolution_clock::now();
        cout<<"info depth "<<depth<<" "<<"scorecp "<<bestMove.first*100<<" time "<<std::chrono::duration_cast<milliseconds>(NowTime - startTime).count()<<endl;
        
        if ((bestMove.first==(2*whitemove-1)*1e5) || (std::chrono::duration_cast<milliseconds>(std::chrono::high_resolution_clock::now() - startTime).count() >= maxtimeinmilli)) {  
            break;
        }
    }
    cout<<"-------------------------------------------"<<endl;
    
    string uci_move = uci::moveToUci(bestMove.second);
    sendResponse("bestmove " + uci_move);

}

void handleQuit() {
    // Clean up and exit
    exit(0);
}



int main() {
    std::string command;
    while (std::getline(std::cin, command)) {
        if (command == "uci") {
            handleUci();
        } 
        else if (command == "isready") {
            handleIsReady();
        } 
        else if (command.substr(0, 8) == "position") {
            handlePosition(command);
        } 
        else if(command.substr(0, 11) == "go movetime"){
            istringstream iss(command);
            string goCommand, movetimeKeyword;
            int maxTimeInMillis = 10000;
            iss >> goCommand >> movetimeKeyword >> maxTimeInMillis;
            cout<<"Max time per move: "<<maxTimeInMillis<<endl;
            handleGo(maxTimeInMillis);
        }
        else if(command.substr(0, 2) == "go") {
            handleGo(10000);
        } 
        else if (command == "quit") {
            handleQuit();
        }
    }
    return 0;
}