#include "chess.hpp"

using namespace chess;
using namespace std;





int countPieces(Board board) {
    Bitboard bitboard = board.us(board.sideToMove());
    return __builtin_popcountll(board.us(board.sideToMove()).getBits()) + __builtin_popcountll(board.them(board.sideToMove()).getBits());
}


int main () { 
    cout<<int(9.2)<<endl;
    Board board = Board("rnbqkbnr/pppp1ppp/8/8/8/8/PPPP1PPP/RN1QKBNR w KQkq - 0 1");



    cout<<countPieces(board)<<endl;


    for (int i=0; i<64; i++){
        if (i%8==0){
            cout<<endl;
        }
        cout<<Square(i)<<" ";
        
    }
    cout<<endl;
    return 0;
}