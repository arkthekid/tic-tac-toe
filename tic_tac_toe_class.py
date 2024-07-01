from random import randint
import math


class tic_tac_toe_terminal:

    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.player2_type = ""
        self.bot_difficulty = ""
        self.player1 = "X"
        self.player2 = "O"
    
    # printing the tic tac toe board
    def print_board(self):
        print("")
        print(f"  {self.board[0][0]}  |  {self.board[0][1]}  |  {self.board[0][2]}  ")
        print("-----------------")
        print(f"  {self.board[1][0]}  |  {self.board[1][1]}  |  {self.board[1][2]}  ")
        print("-----------------")
        print(f"  {self.board[2][0]}  |  {self.board[2][1]}  |  {self.board[2][2]}  ")
        print("")
    
    # reads user input. If invalid, asks again. If valid, places the move on the board. 
    def player_input(self, player):
        player_str = "Player 1" if player==self.player1 else "Player 2"
        print(f"{player_str}'s move (Enter a number between 1-9):")
        move = int(input())-1
        move_row = move//3
        move_col = move%3
        while (((move<0) and (move>8)) or (self.board[move_row][move_col] != " ")):
            print("Your input is invalid. Enter another number:")
            move = int(input())-1
            move_row = move//3
            move_col = move%3   
        self.board[move_row][move_col] = player

    # function for main player's input
    def player1_move(self):
        self.player_input(self.player1)
    
    # function for other player/bot's move
    def player2_move(self):
        if (self.player2_type == "player"):
            self.player_input(self.player2)
        elif (self.bot_difficulty == "easy"):
            bot_move = randint(0, 8)
            bot_move_row = bot_move//3
            bot_move_col = bot_move%3
            while (((bot_move<0) and (bot_move>8)) or (self.board[bot_move_row][bot_move_col] != " ")):
                bot_move = randint(0, 8)
                bot_move_row = bot_move//3
                bot_move_col = bot_move%3
            self.board[bot_move_row][bot_move_col] = self.player2
        elif (self.bot_difficulty == "hard"):
            [bot_move_row, bot_move_col] = self.find_best_move(self.board, self.player2)
            self.board[bot_move_row][bot_move_col] = self.player2

    # Uses the minmax algorithm. If bot's turn, maximizes. If player's turn, minimizes. 
    def minimax(self, board, maximizing, depth, player):
        opponent = "X" if player=="O" else "O"
        score = self.check_board(board, player, opponent)
        

        # checks for game win
        if (score == 1) or (score == -1):
            return score

        # checks for a draw, which is no moves left
        if (self.check_moves_left(board) == False):
            return 0
        
        # player's turn. Maximizing
        if (maximizing):
            best = -100

            # traversing all cells
            for row in range(3):
                for col in range(3):

                    # checks if the box is empty
                    if (board[row][col] == " "):
                        
                        # makes the move
                        board[row][col] = player

                        # calls minimax recursively and takes highest value
                        best = max(best, self.minimax(board, (not maximizing), depth+1, player))

                        # undos move
                        board[row][col] = " "
            return best
        
        # opponent's turn. Minimizing
        if (not maximizing):
            best = 100

            # traversing all cells
            for row in range(3):
                for col in range(3):

                    # checks if the box is empty
                    if (board[row][col] == " "):
                        
                        # makes the move
                        board[row][col] = opponent

                        # calls minimax recursively and takes highest value
                        best = min(best, self.minimax(board, (not maximizing), depth+1, player))

                        # undos move
                        board[row][col] = " "
            return best

    # bot difficulty hard ai function. 
    def find_best_move(self, board, player):
        best_val = -100
        best_move = [-1, -1]

        # traverse through all boxes and run minimax. Return cell with best value.
        for row in range(3):
            for col in range(3):
                
                # checks if cell is empty
                if (self.board[row][col] == " "):

                    # makes the move
                    self.board[row][col] = player

                    # computes the value of the move
                    board = [row[:] for row in self.board]
                    move_val = self.minimax(board, False, 0, player)
                    
                    # undos move
                    self.board[row][col] = " "

                    if move_val > best_val:
                        best_val = move_val
                        best_move = [row, col]
        return best_move

    # checks for draw, meaning no moves left.
    def check_moves_left(self, board):
        for col in range(3):
            for row in range(3):
                if (board[col][row] == " "):
                    return True
        return False

    # checks the status of the game. Doesn't check for draw.
    def check_board(self, board, winner, loser):

        # checks for player1 win! 
        for row in range(3):
            if ((board[row][0] == winner) and (board[row][1] == winner) and (board[row][2] == winner)):
                return 1
        for col in range(3):
            if ((board[0][col] == winner) and (board[1][col] == winner) and (board[2][col] == winner)):
                return 1
        if ((board[0][0] == winner) and (board[1][1] == winner) and (board[2][2] == winner)):
            return 1
        if ((board[0][2] == winner) and (board[1][1] == winner) and (board[2][0] == winner)):
            return 1

        # checks for player1 lost :(
        for row in range(3):
            if ((board[row][0] == loser) and (board[row][1] == loser) and (board[row][2] == loser)):
                return -1
        for col in range(3):
            if ((board[0][col] == loser) and (board[1][col] == loser) and (board[2][col] == loser)):
                return -1
        if ((board[0][0] == loser) and (board[1][1] == loser) and (board[2][2] == loser)):
            return -1
        if ((board[0][2] == loser) and (board[1][1] == loser) and (board[2][0] == loser)):
            return -1

        # no win or loss
        return 0

    # gets player2 type
    def get_player2_type(self):
        print("Do you want to play against a bot or a player? (bot/player):")
        choice = input().lower()
        while ((choice != "bot") and (choice != "player")):
            print("Your input is invalid. Enter 'bot' or 'player:")
            choice = input().lower()
        self.player2_type = choice
        if (self.player2_type == "bot"):
            print("Enter bot difficulty (easy/hard):")
            dif = input().lower()
            while ((dif != "easy") and (dif != "hard")):
                print("Your input is invalid. Enter 'easy' or 'hard:")
                dif = input().lower()
            self.bot_difficulty = dif

    def game_status(self, score, moves_left, player2_type):
        if (player2_type=="bot"):
            if (not moves_left) and (score == 0):
                return "Draw"
            elif (score == 1):
                return "You win!"
            elif (score == -1):
                return "You lose :("
        else:
            if (not moves_left) and (score == 0):
                return "Draw"
            elif (score == 1):
                return "Player 1 wins!"
            elif (score == -1):
                return "Player 2 wins!"

    # game driver 
    def start_game(self):
        self.get_player2_type()
        self.player1_move()
        self.print_board()
        score = self.check_board(self.board, self.player1, self.player2)
        moves_left = self.check_moves_left(self.board)
        while (moves_left) and (score == 0):
            self.player2_move()
            self.print_board()
            score = self.check_board(self.board, self.player1, self.player2)
            moves_left = self.check_moves_left(self.board)
            if (not moves_left) or (score != 0):
                print(self.game_status(score, moves_left, self.player2_type))
                return           
            self.player1_move()
            self.print_board()
            score = self.check_board(self.board, self.player1, self.player2)
            moves_left = self.check_moves_left(self.board)
        print(self.game_status(score, moves_left, self.player2_type))

class tic_tac_toe_gui:

    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.op_type = ""
        self.bot_difficulty = ""
        self.player1 = "X"
        self.player2 = "O"
    
    # reads user input. If invalid, asks again. If valid, places the move on the board. 
    def player_input(self, player):
        player_str = "Player 1" if player==self.player1 else "Player 2"
        print(f"{player_str}'s move (Enter a number between 1-9):")
        move = int(input())-1
        move_row = move//3
        move_col = move%3
        while (((move<0) and (move>8)) or (self.board[move_row][move_col] != " ")):
            print("Your input is invalid. Enter another number:")
            move = int(input())-1
            move_row = move//3
            move_col = move%3   
        self.board[move_row][move_col] = player

    # function for main player's input
    def player1_move(self):
        self.player_input(self.player1)
    
    # function for other player/bot's move
    def player2_move(self):
        if (self.op_type == "player"):
            self.player_input(self.player2)
        elif (self.bot_difficulty == "easy"):
            bot_move = randint(0, 8)
            bot_move_row = bot_move//3
            bot_move_col = bot_move%3
            while (((bot_move<0) and (bot_move>8)) or (self.board[bot_move_row][bot_move_col] != " ")):
                bot_move = randint(0, 8)
                bot_move_row = bot_move//3
                bot_move_col = bot_move%3
            self.board[bot_move_row][bot_move_col] = self.player2
        elif (self.bot_difficulty == "hard"):
            [bot_move_row, bot_move_col] = self.find_best_move(self.board, self.player2)
            self.board[bot_move_row][bot_move_col] = self.player2
    
    # function for other player/bot's move
    def bot_move(self):
        if (self.bot_difficulty == "easy"):
            bot_move = randint(0, 8)
            bot_move_row = bot_move//3
            bot_move_col = bot_move%3
            while (((bot_move<0) and (bot_move>8)) or (self.board[bot_move_row][bot_move_col] != " ")):
                bot_move = randint(0, 8)
                bot_move_row = bot_move//3
                bot_move_col = bot_move%3
            self.board[bot_move_row][bot_move_col] = self.player2
            return [bot_move_row, bot_move_col]
        elif (self.bot_difficulty == "hard"):
            [bot_move_row, bot_move_col] = self.find_best_move(self.board, self.player2)
            self.board[bot_move_row][bot_move_col] = self.player2
            return [bot_move_row, bot_move_col]

    # Uses the minmax algorithm. If bot's turn, maximizes. If player's turn, minimizes. 
    def minimax(self, board, maximizing, depth, player):
        opponent = "X" if player=="O" else "O"
        score = self.check_board(board, player, opponent)
        

        # checks for game win
        if (score == 1) or (score == -1):
            return score

        # checks for a draw, which is no moves left
        if (self.check_moves_left(board) == False):
            return 0
        
        # player's turn. Maximizing
        if (maximizing):
            best = -100

            # traversing all cells
            for row in range(3):
                for col in range(3):

                    # checks if the box is empty
                    if (board[row][col] == " "):
                        
                        # makes the move
                        board[row][col] = player

                        # calls minimax recursively and takes highest value
                        best = max(best, self.minimax(board, (not maximizing), depth+1, player))

                        # undos move
                        board[row][col] = " "
            return best
        
        # opponent's turn. Minimizing
        if (not maximizing):
            best = 100

            # traversing all cells
            for row in range(3):
                for col in range(3):

                    # checks if the box is empty
                    if (board[row][col] == " "):
                        
                        # makes the move
                        board[row][col] = opponent

                        # calls minimax recursively and takes highest value
                        best = min(best, self.minimax(board, (not maximizing), depth+1, player))

                        # undos move
                        board[row][col] = " "
            return best

    # bot difficulty hard ai function. 
    def find_best_move(self, board, player):
        best_val = -100
        best_move = [-1, -1]

        # traverse through all boxes and run minimax. Return cell with best value.
        for row in range(3):
            for col in range(3):
                
                # checks if cell is empty
                if (self.board[row][col] == " "):

                    # makes the move
                    self.board[row][col] = player

                    # computes the value of the move
                    board = [row[:] for row in self.board]
                    move_val = self.minimax(board, False, 0, player)
                    
                    # undos move
                    self.board[row][col] = " "

                    if move_val > best_val:
                        best_val = move_val
                        best_move = [row, col]
        return best_move

    # checks for draw, meaning no moves left.
    def check_moves_left(self, board):
        for col in range(3):
            for row in range(3):
                if (board[col][row] == " "):
                    return True
        return False

    def get_winning_boxes(self):
        # checks for player1 win
        for row in range(3):
            if ((self.board[row][0] == "X") and (self.board[row][1] == "X") and (self.board[row][2] == "X")):
                return [row, 0], [row, 1], [row, 2]
        for col in range(3):
            if ((self.board[0][col] == "X") and (self.board[1][col] == "X") and (self.board[2][col] == "X")):
                return [0, col], [1, col], [2, col]
        if ((self.board[0][0] == "X") and (self.board[1][1] == "X") and (self.board[2][2] == "X")):
            return [0, 0], [1, 1], [2, 2]
        if ((self.board[0][2] == "X") and (self.board[1][1] == "X") and (self.board[2][0] == "X")):
            return [0, 2], [1, 1], [2, 0]

        # checks for player1 lose
        for row in range(3):
            if ((self.board[row][0] == "O") and (self.board[row][1] == "O") and (self.board[row][2] == "O")):
                return [row, 0], [row, 1], [row, 2]
        for col in range(3):
            if ((self.board[0][col] == "O") and (self.board[1][col] == "O") and (self.board[2][col] == "O")):
                return [0, col], [1, col], [2, col]
        if ((self.board[0][0] == "O") and (self.board[1][1] == "O") and (self.board[2][2] == "O")):
            return [0, 0], [1, 1], [2, 2]
        if ((self.board[0][2] == "O") and (self.board[1][1] == "O") and (self.board[2][0] == "O")):
            return [0, 2], [1, 1], [2, 0]
    
    # checks the status of the game. Doesn't check for draw.
    def check_board(self, board, winner, loser):

        # checks for player1 win
        for row in range(3):
            if ((board[row][0] == winner) and (board[row][1] == winner) and (board[row][2] == winner)):
                return 1
        for col in range(3):
            if ((board[0][col] == winner) and (board[1][col] == winner) and (board[2][col] == winner)):
                return 1
        if ((board[0][0] == winner) and (board[1][1] == winner) and (board[2][2] == winner)):
            return 1
        if ((board[0][2] == winner) and (board[1][1] == winner) and (board[2][0] == winner)):
            return 1

        # checks for player1 lose
        for row in range(3):
            if ((board[row][0] == loser) and (board[row][1] == loser) and (board[row][2] == loser)):
                return -1
        for col in range(3):
            if ((board[0][col] == loser) and (board[1][col] == loser) and (board[2][col] == loser)):
                return -1
        if ((board[0][0] == loser) and (board[1][1] == loser) and (board[2][2] == loser)):
            return -1
        if ((board[0][2] == loser) and (board[1][1] == loser) and (board[2][0] == loser)):
            return -1

        # no win or loss
        return 0


    def game_status(self, score, moves_left, player2_type):
        if (player2_type=="bot"):
            if (not moves_left) and (score == 0):
                return "Draw"
            elif (score == 1):
                return "You win!"
            elif (score == -1):
                return "You lose :("
        else:
            if (not moves_left) and (score == 0):
                return "Draw"
            elif (score == 1):
                return "Player 1 wins!"
            elif (score == -1):
                return "Player 2 wins!"

    def is_box_available(self, board_row, board_col):
        if (self.board[board_row][board_col] == " "):
            return True
        return False

    # game driver 
    def start_game(self):
        self.get_player2_type()
        self.player1_move()
        #self.retrieve_board()
        score = self.check_board(self.board, self.player1, self.player2)
        moves_left = self.check_moves_left(self.board)
        while (moves_left) and (score == 0):
            self.player2_move()
            score = self.check_board(self.board, self.player1, self.player2)
            moves_left = self.check_moves_left(self.board)
            if (not moves_left) or (score != 0):
                print(self.game_status(score, moves_left, self.op_type))
                return           
            self.player1_move()
            #self.retrieve_board()
            score = self.check_board(self.board, self.player1, self.player2)
            moves_left = self.check_moves_left(self.board)
        print(self.game_status(score, moves_left, self.op_type))
