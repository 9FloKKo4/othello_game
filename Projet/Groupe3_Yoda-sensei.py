import random
from copy import deepcopy


class  Yoda_sensei:    
    def __init__(self):
        self.name = "YODA-sensei"
        self.opening_moves_black =  [ 
            [[3, 2], [2, 3], [3, 3], [2, 2]],
            [[2, 2], [4, 2], [2, 4], [4, 4],[5,3]],
            [[3, 2], [2, 3], [4, 4], [5, 5], [6, 6]],
            [[3, 5], [5, 3], [4, 2], [2, 4], [6, 4]],
            [[2, 5], [5, 2], [4, 5], [5, 4], [3, 2]],
        ]
             
        self.opening_moves_white=  [
            [[4, 2], [5, 3], [4, 3], [3,4],[3,3]],
            [[2, 3], [2, 4], [3, 2], [4, 5], [5, 4]],
            [[3, 3], [4, 3], [4, 4], [5, 3], [5, 4],[4,5]],
            [[3, 2], [2, 3], [2, 2], [2, 5],
            [6, 3], [3, 6], [6, 5], [5, 6], [6, 6],[4,3]],
             ]
      
      
    def check_turn(self,Game):
        turn= (Game.score_black+Game.score_white)-4
        return turn
     


    def check_valid_moves(self,othello_board,othello_game):
        

        new_board= Board(8)
        new_board.create_board()
        weight_board=[
            100, -20, 10, 5, 5, 10, -20, 100,
            -20, -50, -2, -2, -2, -2, -50, -20,
            10, -2, -1,-1,-1, -1, -2, 10,
            5, -2,-1,-1,-1,-1, -2, 5,
            5, -2,-1,-1,-1,-1, -2, 5,
            10, -2, -1,-1,-1, -1, -2, 10,   
            -20, -50, -2, -2, -2, -2, -50, -20,
            100, -20, 10, 5, 5, 10, -20, 100]
       # cerate Board
        for tile in range(len(new_board.board)):
             new_board.board[tile].weight= weight_board[tile]
             
        possible_moves=[]
        corner_spaces =  [[0, 0], [0, 7], [7, 0], [7, 7]]
        adjacent_spots = [[0, 1], [1, 0], [1, 1], [1, 6], [0, 6], [1, 7], [6, 0], [6, 1], [6, 6], [7, 1], [6, 7], [7, 6]]
   

        max_points=-10000

       
       
        for element_tile in range(len(othello_board.board)):
            legal = othello_board.is_legal_move(othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos,othello_game.active_player)
        
               
            if legal != False:
                move_points= 0
                pos_x_y =othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos
                
                if pos_x_y in corner_spaces and pos_x_y not in adjacent_spots  :
                    move_points += 20
                    possible_moves.append([othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos, move_points]) 
                    
                     
                for point in  legal:
                # Sur chacune des directions, on récupère la liste
                    move_points += point[0] 
                move_points += new_board.board[element_tile].weight
                     # On fait la somme pour toutes les directions   
                current_turn = self.check_turn(othello_game)  
                if current_turn < 5:
                    if othello_game.active_player == "⚫":
                        self.opening_moves_black[current_turn]
                        for count_turn in   self.opening_moves_black[current_turn]:
                         if count_turn == [othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos]:
                            move_points =+ 100
                    else :
                        self.opening_moves_white[current_turn]
                        for count_turn in   self.opening_moves_white[current_turn]:
                         if count_turn == [othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos]:
                            move_points =+ 100
                        

                if max_points== move_points:
                   possible_moves.append([othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos,move_points])
                elif max_points < move_points:
                    max_points= move_points
                    possible_moves= [[othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos,move_points]]
               
           
         
        return random.choice(possible_moves)
    


    
    grp3_bot = Yoda_sensei()
    move_coordinates= grp3_bot.check_valid_moves(othello_board,othello_game)