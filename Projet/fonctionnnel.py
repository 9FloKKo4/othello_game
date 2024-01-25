import random
from copy import deepcopy 

# Object used to create new boards


class Board:
    def __init__(self, size):
        self.size = size
        self.board = []

    # Used to fill the "board" property with a list with a length equal to the "size" property
    def create_board(self):
        for y_pos in range(self.size):
            for x_pos in range(self.size):
                #  Create a Tile instance
                #  Gives it the coordinates (depending on x_pos and y_pos)
                #  Add it to the board property
                if x_pos != 0 and x_pos != 7 and y_pos != 0 and y_pos != 7:
                    self.board.append(Tile(x_pos, y_pos, "🟩", "🟩"))
                else:
                    self.board.append(Tile(x_pos, y_pos, "X", "🟩"))
        self.place_initial_pawns()

    #  This will print the game board, depending on the data_type
    #  Data types are "Coordinates", "Type" and "Content"
    def draw_board(self, data_type):
        display_board = []
        line_breaker = 0
        print([0, ' 0', ' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7'])
        for board_index in self.board:
            if (board_index.x_pos == 0):
                display_board.append(board_index.y_pos)
            if data_type == "Coordinates":
                display_board.append([board_index.x_pos, board_index.y_pos])
            elif data_type == "Type":
                display_board.append(board_index.type)
            else:
                display_board.append(board_index.content)
            line_breaker += 1
            if line_breaker > 7:
                print(display_board)
                line_breaker = 0
                display_board = []
        print("\n")

    # Place the 4 initial pawns at the center of the board (2 white and 2 black)
    def place_initial_pawns(self):
        #  We pick the 4 central tiles
        #  And place 2 black pawns and 2 white pawns
        self.board[27].content = "⚪"
        self.board[28].content = "⚫"
        self.board[35].content = "⚫"
        self.board[36].content = "⚪"

    # Check if the position in inside the board
    # Return true or false depending if it is inside or not
    def is_on_board(self, x_pos, y_pos):
        if x_pos < 0 or x_pos > 7 or y_pos < 0 or y_pos > 7:
            return False
        else:
            return True

    # Check if the tile is an empty tile ("🟩")
    # Return true or false depending if it is empty or not
    def is_tile_empty(self, x_pos, y_pos):
        if self.board[(x_pos) + y_pos * 8].content == "🟩":
            return True
        else:
            return False

    # Takes a position (x_pos, y_pos) and a color
    # Try to simulate the move
    # Returns either false if the move is not valid
    # Or returns which pawns will change color if true
    # The returned list will contain [numbers_of_pawns_to_change, [direction_x, direction_y]]
    def is_legal_move(self, x_pos, y_pos, color):

        # North / Nort-East / East / South-East / South / South-West / West / North-West
        directions = [
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
            [-1, 0],
            [-1, -1],
        ]

        # Opposite of the color of the placed pawn
        if color == "⚪":
            awaited_color = "⚫"
        else:
            awaited_color = "⚪"

        current_x_pos = x_pos
        current_y_pos = y_pos
        is_legal = False
        # [number_of_tile_to_flip, direction]
        # Si on a un pion noir placé en 2,3, on veut:
        # [[1, [1, 0]]
        tiles_to_flip = []

        if (not self.is_tile_empty(current_x_pos, current_y_pos) or not self.is_on_board(current_x_pos, current_y_pos)):
            return False

        # Check for every direction
        for current_dir in directions:
            number_of_tiles_to_flip = 1
            # Get your original coordinates + the direction modifier
            current_x_pos = x_pos + current_dir[0]
            current_y_pos = y_pos + current_dir[1]
            # Check if the new position is on the board and empty
            if self.is_on_board(current_x_pos, current_y_pos):
                #  Get the tile informations
                current_index = self.board[current_x_pos + current_y_pos * 8]
                # If the tile contains a pawn of the opposite color, continue on the line
                while current_index.content == awaited_color:
                    current_x_pos += current_dir[0]
                    current_y_pos += current_dir[1]
                    if self.is_on_board(current_x_pos, current_y_pos):
                        current_index = self.board[current_x_pos +
                                                   current_y_pos * 8]
                        # If the line ends with a pawn of your color, then the move is legal
                        if current_index.content == color:
                            is_legal = True
                            tiles_to_flip.append(
                                [number_of_tiles_to_flip, current_dir])
                            break
                    else:
                        break
                    number_of_tiles_to_flip += 1

        if is_legal:
            return tiles_to_flip
        else:
            return False

    # Takes a position (x_pos, y_pos), an array with a number of tiles to flip and a direction, and a color
    # The array should be obtained with the "is_legal_move" function
    # Doesn't return anything, but will change the color of the tiles selected by "tiles_to_flip"
    def flip_tiles(self, x_pos, y_pos, tiles_to_flip, color):
        # x_pos and y_pos = new pawn position
        # tiles_to_flip = list containing the number of pawn to flip and a direction
        # ex: [
        # [1, [1, 0]],
        # ] means we're changing 1 pawn to the right
        # color = the new color of the pawns to flip
        for current_dir in tiles_to_flip:
            current_x_pos = x_pos + current_dir[1][0]
            current_y_pos = y_pos + current_dir[1][1]
            for nb_tile in range(current_dir[0]):
                current_index = self.board[current_x_pos + current_y_pos * 8]
                current_index.content = color
                current_x_pos += current_dir[1][0]
                current_y_pos += current_dir[1][1]

# Used to create each tile of your board
# Contains a position (x, y), a type to check if it's a boder tile or not, and a content to check if there is a pawn inside the tile


class Tile:
    #   Type is used to check if its an "🟩" empty tile or a "X" border tile
    #   Content is used to check if a pawn is placed o (Empty), B (Black), W (White)
    def __init__(self, x_pos, y_pos, type, content):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = type
        self.content = content

# Used to create new ruleset
# Contains the score, the active player, the game_over check and functions allowing to interact with the game
   

class Game:
    def __init__(self):
        self.score_black = 2
        self.score_white = 2
        self.active_player = "⚫"
        self.is_game_over = False
        self.winner = "Noone"

    # Place a pawn on the board (checks if the move is legal before placing it)
    # It takes a position (x, y), a Board object instance and a color
    # The function will automatically check if the move is valid or not
    def place_pawn(self, x_pos, y_pos, board_instance, color):
        if not board_instance.is_on_board(x_pos, y_pos):
            print("Coordinates outside the board")
        else:
            if board_instance.board[(x_pos) + y_pos * 8].content == "🟩":
                tiles_to_flip = board_instance.is_legal_move(   
                    x_pos, y_pos, color)
                if not tiles_to_flip:
                    print("Invalid move")
                else:
                    board_instance.board[(x_pos) + y_pos * 8].content = color
                    board_instance.flip_tiles(
                        x_pos, y_pos, tiles_to_flip, color)
                    print(f"Pion placé en {x_pos}, {y_pos}")
                    self.update_score(board_instance)
                    self.change_active_player()
                    self.check_for_valid_moves(board_instance)
                    board_instance.draw_board("Content")
            else:
                print("There is already a pawn here")

    # Change the active player color from black to white or white to black
    def change_active_player(self):
        # Prend self.active_player et change la couleur du joueur actif
        if self.active_player == "⚫":
            self.active_player = "⚪"
            print("C'est au tour du joueur blanc")
        else:
            self.active_player = "⚫"
            print("C'est au tour du joueur noir")

    # Update the players score after a successful move
    def update_score(self, board_instance):
        # Count all the black & white pawns, and update the scores
        w_score = 0
        b_score = 0
        for tile_index in board_instance.board:
            if tile_index.content == "⚪":
                w_score += 1
            elif tile_index.content == "⚫":
                b_score += 1
        self.score_black = b_score
        self.score_white = w_score

    # Check for a valid move, and end the game if there is none for the current player
    def check_for_valid_moves(self, board_instance):
        is_game_over = True
        for tile_index in board_instance.board:
            move_to_check = board_instance.is_legal_move(
                tile_index.x_pos, tile_index.y_pos, self.active_player)
            if move_to_check != False:
                is_game_over = False

        if is_game_over:
            self.check_for_winner()
            self.is_game_over = True

    # Compare the score, and print the winner's color
    def check_for_winner(self):
        print("Partie terminée !")
        print("Le joueur noir a: " + str(self.score_black) + " points")
        print("Le joueur white a: " + str(self.score_white) + " points")
        if (self.score_black > self.score_white):
            print("Le joueur noir a gagné !")
            self.winner = "⚫"
        elif (self.score_white > self.score_black):
            print("Le joueur blanc a gagné !")
            self.winner = "⚪"
        else:
            print("Égalité !")




    
    class OthelloStrategy:
        def __init__(self):
            pass

        def mobility(self, player_moves, opponent_moves):
            return len(player_moves) - len(opponent_moves)

        def evaporation(self, player_moves, opponent_moves):
            # Force the opponent to flip many discs
            return len(opponent_moves) - len(player_moves)

        def is_quiet_move(self, move, othello_board):
            # Check if a move is a quiet move (does not flip border discs)
            return all(not othello_board.is_border(x, y) for x, y in move)

        def find_quiet_moves(self, legal_moves, othello_board):
            # Find quiet moves among the legal moves
            return [move for move in legal_moves if self.is_quiet_move(move, othello_board)]

        def opening_strategy(self, othello_board, player, opponent):
            player_moves = othello_board.is_legal_moves(player)
            opponent_moves = othello_board.is_legal_moves(opponent)

            mobility_score = self.mobility(player_moves, opponent_moves)
            evaporation_score = self.evaporation(player_moves, opponent_moves)

            if mobility_score > 0:
                # Maximize mobility
                return max(player_moves, key=lambda move: len(opponent.get_flips(move[0], move[1])))
            elif evaporation_score > 0:
                # Force opponent to flip many discs (evaporation)
                return max(player_moves, key=lambda move: len(opponent.get_flips(move[0], move[1])))
            else:
                # No clear strategy, play a quiet move
                quiet_moves = self.find_quiet_moves(player_moves, othello_board)
                return quiet_moves[0] if quiet_moves else player_moves[0]
    
    def remove_access(self, move, othello_board, player):
        # Remove access to a square by flipping necessary discs
        flips = player.get_flips(move[0], move[1])
        for flip in flips:
            othello_board.flip_disc(flip[0], flip[1])

    def opening_inoue(self, othello_board, player, opponent):
        player_moves = othello_board.is_legal_moves(player)
        opponent_moves = othello_board.is_legal_moves(opponent)

        quiet_moves = self.find_quiet_moves(player_moves, othello_board)

        if quiet_moves:
            # Play a quiet move if available
            return quiet_moves[0]
        else:
            # No quiet moves, try to remove opponent's access
            opponent_quiet_moves = self.find_quiet_moves(opponent_moves, othello_board)
            if opponent_quiet_moves:
                # Remove access to opponent's quiet move
                self.remove_access(opponent_quiet_moves[0], othello_board, player)
            # Play a random legal move as a fallback
            return player_moves[0]


class Bot:
    def __init__(self):
        self.name = "Yoda_sensei F"
        self.opening_black_moves = [
            [[2, 3], [2, 4], [3, 2], [5, 4], [4, 5]],
            [[2, 3], [2, 4], [3, 2], [5, 4], [4, 5]],
            [[2, 3], [2, 4], [3, 2], [5, 4], [4, 5]],
            [[2, 3], [2, 4], [3, 2], [5, 4], [4, 5]],
            [[2, 3], [2, 4], [3, 2], [5, 4], [4, 5]]
        ] 

    def count_discs_difference(self, othello_board):
        black_discs = 0
        white_discs = 0
        for tile in othello_board.board:
            if tile.color == "black":
                black_discs += 1
            elif tile.color == "white":
                white_discs += 1
        return black_discs - white_discs

    def center_moves(self, othello_board):
        center_moves = [[3, 2], [2, 3], [3, 3], [4, 3], [3, 4]]
        legal_moves = []
        for move in center_moves:
            if othello_board.is_legal_move(move[0], move[1], self.name):
                possible_moves.append(move)
        return possible_moves

    def avoid_frontier_moves(self, othello_board):
        frontier_moves = []
        for tile in othello_board.board:
            if tile.is_frontier():
                frontier_moves.append([tile.x_pos, tile.y_pos])
        legal_moves = []
        for move in frontier_moves:
            if othello_board.is_legal_move(move[0], move[1], self.name):
                legal_moves.append(move)
        return legal_moves

    def group_discs(self, othello_board):
        # Implementation needed based on board analysis
        pass

    def avoid_early_edges(self, othello_board, othello_game):
        turn = (othello_game.score_black + othello_game.score_white) - 4
        if turn < 25:  # Adjust the turn threshold as needed
            edge_moves = [[0, 2], [2, 0], [5, 7], [7, 5]]
            legal_moves = []
            for move in edge_moves:
                if othello_board.is_legal_move(move[0], move[1], self.name):
                    legal_moves.append(move)
            return legal_moves
        else:
            return []


    # BOT FUNCTIONS
    def check_turn(self, Game):
        turn = (Game.score_black + Game.score_white) - 4
        return turn

    def create_new_board(self, board_bis):
        matrice_list = [
            100, -20, 10, 5, 5, 10, -20, 100,
            -20, -50, -2, -2, -2, 10, -50, -20,
            10, -2, -1, -1, -1, -1, -2, 10,
            5, -2, -1, -1, -1, -1, -2, 5,
            5, -2, -1, -1, -1, -1, -2, 5,
            10, -2, -1, -1, -1, -1, -2, 10,
            -20, -50, -2, -2, -2, 10, -50, -20,
            100, -20, 10, 5, 5, 10, -20, 100]
        for list_index_new in range(len(board_bis.board)):
            board_bis.board[list_index_new].weight = matrice_list[list_index_new]

    def check_valid_moves(self, othello_board, othello_game):
        possible_moves = []
        corner_spaces = [[0, 0], [0, 7], [7, 0], [7, 7]]
        central_moves = [[3, 2], [2, 3], [3, 3], [4, 3], [3, 4]]
        max_points = -1000
        move_points = 0
        board_bis = Board(8)
        board_bis.create_board()
        self.create_new_board(board_bis)
        

        for element_tile in range(len(othello_board.board)):
            legal = othello_board.is_legal_move(
                othello_board.board[element_tile].x_pos, othello_board.board[element_tile].y_pos,
                othello_game.active_player)

            if legal != False:
                move_points = 0

                # Corner play
                if [othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos] in corner_spaces:
                    possible_moves.append([othello_board.board[element_tile].x_pos, othello_board.board[element_tile].y_pos])

                # Damiérisation
                for move_in_center in central_moves:
                    if move_in_center in legal:
                        possible_moves.append(move_in_center)

                for count_points in legal:
                    move_points += count_points[0]
                move_points += board_bis.board[element_tile].weight

                current_turn = self.check_turn(othello_game)
                if current_turn < 5:
                    self.opening_black_moves[current_turn]
                    for count_turn in self.opening_black_moves[current_turn]:
                        if count_turn == [othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos]:
                            move_points += 100

                if max_points == move_points:
                    possible_moves.append(
                        [othello_board.board[element_tile].x_pos, othello_board.board[element_tile].y_pos])

                elif max_points < move_points:
                    max_points = move_points
                    possible_moves = [[othello_board.board[element_tile].x_pos, othello_board.board[element_tile].y_pos]]
                print("In", othello_board.board[element_tile].x_pos, othello_board.board[element_tile].y_pos,"Score + weight =", move_points)


        return random.choice(possible_moves)


    
     

        

    
    
class Botus:
    def __init__(self):
        self.name = "YODA-sensei S"
        self.opening_moves_black =  [
        [[3, 2], [2, 3], [3, 3], [4, 3]],
        [[2, 2], [4, 2], [2, 4], [4, 4],[5,3]],
        [[3, 2], [2, 3], [4, 4], [5, 5], [6, 6]],
        [[3, 5], [5, 3], [4, 2], [2, 4], [6, 4]],
        [[2, 5], [5, 2], [4, 5], [5, 4], [3, 2]],
            ]
        self.opening_moves_white=  [
        [[3, 3], [4, 3], [3, 4], [4,4 ]],
        [[2, 3], [2, 4], [3, 2], [4, 5], [5, 4]],
        [[3, 3], [4, 3], [4, 4], [5, 3], [5, 4],[4,5]],
        [[3, 2], [2, 3], [2, 2], [2, 5]],
        [[6, 3], [3, 6], [6, 5], [5, 6], [6, 6]],
            ]
      # BOT FUNCTIONS
    def check_turn(self,Game):
        turn= (Game.score_black+Game.score_white)-4
        return turn
     

    def check_valid_moves(self,othello_board,othello_game,depth):
        new_board= Board(8)
        new_board.create_board()
        weight_board=[
            100,-10,10,5,5,10,-10,100,
            -10,-20,3,3,3,3,-20,-10,
            10,3,15,2,2,15,3,10,
            5,3,2,-1,-1,2,3,5,
            5,3,2,-1,-1,2,3,5,
            10,3,2,2,2,2,3,10,   
            -10,-20,3,3,3,3,-20,-10,
            100,-10,10,5,5,10,-10,100] 
       
        for tile in range(len(new_board.board)):
             new_board.board[tile].weight= weight_board[tile]
             
        possible_moves=[]
        corner_spaces = [(0, 0), (0, 7), (7, 0), (7, 7)]
        adjacent_spots = [(0, 1), (1, 0),(0, 6), (1, 7),(6, 0), (7, 1),(6, 7), (7, 6)]

        max_points=-10000

        for element_tile in range(len(othello_board.board)):
            legal = othello_board.is_legal_move(othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos,othello_game.active_player)
        
            
            if legal != False:
                move_points= 0
                pos_x_y =othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos
                
                if pos_x_y in corner_spaces and pos_x_y not in adjacent_spots  :
                    move_points += 20
                    possible_moves.append([othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos]) 
                    
                     
                for point in  legal:
                # Sur chacune des directions, on récupère la liste
                    move_points += point[0] 
                move_points += new_board.board[element_tile].weight
                # On fait la somme pour toutes les directions   
                current_turn = self.check_turn(othello_game)  
                if current_turn< 5:
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
                
                
                             
                        
# Calcul des points max ETAPE 2
                if max_points == move_points:
                   possible_moves.append([othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos,move_points])
                elif max_points < move_points:
                    max_points= move_points
                    possible_moves= [[othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos,move_points]]
                print("le score + poids=",move_points)
              
            
            if(depth > 0):
                depth -= 1
                for slide in possible_moves:
                    new_board_plus = deepcopy(othello_board)
                    new_game = deepcopy(othello_game)
                    new_game.place_pawn(slide[0], slide[1], new_board_plus, new_game.active_player)
                    if not new_game.is_game_over :
                        opponent_points = self.check_valid_moves(new_board_plus, new_game, depth)
                        slide[2] -= opponent_points[2]
                    possible_moves.sort()
                    
                    # max_opps_points=-1000
                    # move_opps_points = 0
                    # if max_opps_points == move_opps_points:
                    #     possible_moves.append([othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos,move_opps_points])
                    # elif max_opps_points < move_opps_points:
                    #     max_opps_points= move_opps_points
                    # possible_moves= [[othello_board.board[element_tile].x_pos,othello_board.board[element_tile].y_pos,move_opps_points]]
               
                  
                
                   
              
        return random.choice(possible_moves)
        
    print("Il faut récupérer toutes les cases du tableau")
    print("Vérifier quels coups sont jouables")
    print("Et renvoyer les coordonnées")


# Loop until the game is over
def play_games(number_of_games):
    white_victories = 0
    black_victories = 0
    
    for current_game in range(number_of_games):
        # Create a new board & a new game instances
        othello_board = Board(8)
        othello_game = Game()

        # Fill the board with tiles
        othello_board.create_board()

        # Draw the board
        othello_board.draw_board("Content")
        # Create 2 bots
        myBot = Bot()
        otherBot = Botus()

        while not othello_game.is_game_over:
            # First player / bot logic goes here
            if(othello_game.active_player == "⚫"):
                move_coordinates = myBot.check_valid_moves(othello_board,othello_game)
                othello_game.place_pawn(
                move_coordinates[0], move_coordinates[1], othello_board, othello_game.active_player)


            # Second player / bot logic goes here
            else:
                move_coordinates = otherBot.check_valid_moves(othello_board,othello_game, 1) 
                othello_game.place_pawn(
                move_coordinates[0], move_coordinates[1], othello_board, othello_game.active_player)
        
        if(othello_game.winner == "⚫"):
            black_victories += 1
        elif(othello_game.winner == "⚪"):
            white_victories += 1
        
    
    print("End of the games, showing scores: ")
    print("Black player won " + str(black_victories) + " times")
    print("White player won " + str(white_victories) + " times")
        

play_games(15)