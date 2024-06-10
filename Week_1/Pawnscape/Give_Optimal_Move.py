
#current_board is a nXn 2 dimensional list with 0 for empty, 1 for White, 2 for Black
# So the original (4x4) board is [[1,1,1,1],[0,0,0,0],[0,0,0,0],[2,2,2,2]]


# This function returns all the moves for the player to play in the current board
def All_Moves(current_board,playertoplay):
    
    positions_of_playertoplay=[]
    positions_of_playertoface=[]
    empty_positions=[]
    opposition=1+(playertoplay)%2
    n=len(current_board)
    
    for row_number in range(n):
        for column_number in range(len(current_board[row_number])):
            cell=current_board[row_number][column_number]
            if cell==playertoplay:
                positions_of_playertoplay.append([row_number,column_number])
            elif cell==opposition:
                positions_of_playertoface.append([row_number,column_number])
            else:
                empty_positions.append([row_number,column_number])
            
            
    All_Moves=[] #This will contain a list of moves where each move is of the form [[inital_posn_x,inital_posn_y],[final_posn_x,final_posn_y],playertoplay,capturebool]
    for i in range(len(positions_of_playertoplay)):
        rowofplayer=positions_of_playertoplay[i][0]
        columnofplayer=positions_of_playertoplay[i][1]
        initial_posn=[rowofplayer,columnofplayer]
        
        
        if current_board[rowofplayer+1][columnofplayer]==0:
            move=[initial_posn,[rowofplayer+1,columnofplayer],playertoplay,False]
            All_Moves.append(move)
            
        
        
        if (current_board[rowofplayer+1][columnofplayer+1]==opposition & columnofplayer<n-1):
            move=[initial_posn,[rowofplayer+1,columnofplayer+1],playertoplay,True]
            All_Moves.append(move)
            
        if (current_board[rowofplayer+1][columnofplayer-1]==opposition & columnofplayer>0):
            move=[initial_posn,[rowofplayer+1,columnofplayer-1],playertoplay,True]
            All_Moves.append(move)

    return All_Moves



def Update_Board(current_board,move):
    
    
    initial_posn=move[0]
    fineal_posn=move[1]
    playertoplay=move[2]
    capture=move[3]    
    
    current_board[initial_posn[0]][initial_posn[1]]=0
    current_board[final_posn[0]][final_posn[1]]=playertoplay
    
    return current_board
    
    
def Detect_Win(current_board):

    
    for i in current_board[0]:
        if i==2:
            return 2
    
    for i in current_board[-1]:
        if i==1:
            return 1

    return False


    

def Find_Optimal_Move(current_board,playertoplay):
    
    All_Moves=All_Moves(current_board,playertoplay)
    opposition=1+(playertoplay)%2
    new_board_configurations={}
    
    
    
    for i in All_Moves:
        New_Board=Update_Board(current_board,i)
        new_board_configurations[New_Board]=i
    
    
    for i in new_board_configurations:
        if Detect_Win(i):
            return new_board_configurations[New_Board]
    
    # Later code coming later

def All_Games(current_board,playertoplay):
    
    # this will return a list of list of tuple where each list has the tuple (move,new_board)
    # [[(),(),(),(),(),()],[(),(),(),(),(),()],[(),(),(),(),(),()],[(),(),(),(),(),()]]
    
    All_Moves=All_Moves(current_board,playertoplay)
    opposition=1+(playertoplay)%2
    new_board_configurations={}
    
    full_list=[]
    
    for i in All_Moves:
        New_Board=Update_Board(current_board,i)
        new_board_configurations[New_Board]=i
        
        
        
        every=All_Games(New_Board,opposition)
        for i in every:
            new=(i,New_Board)
            

    