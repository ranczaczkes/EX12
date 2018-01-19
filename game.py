from itertools import repeat
import math
import copy
class Game:

    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    ROW_NUMBER = 6
    COL_NUMBER = 7


    def __init__(self):

        self.empty_spaces = [6
                      for i in repeat(None, Game.COL_NUMBER)]
        self.board = {}
        for i in range(Game.COL_NUMBER):
            self.board[i] = [" " for i in repeat(None, Game.ROW_NUMBER)]
        self.current_player = False
        self.last_move = -1


    def make_move(self, column):
        try:
            if column < Game.COL_NUMBER and column >= 0:
                if self.empty_spaces[column] == 0:
                    raise ValueError
            else: raise ValueError
        except ValueError:
            raise Exception("Illegal move.")

        self.empty_spaces[column] -= 1
        self.board[column][self.empty_spaces[column]] = int(self.current_player)
        self.last_move = column
        self.current_player = not self.current_player

    def get_last_move(self):
        return self.last_move

    def get_player_one(self):
        return self.PLAYER_ONE
    def get_player_tow(self):
        return self.PLAYER_TWO

    def get_empty_spaces(self):
        return copy.deepcopy(self.empty_spaces)

    def get_empty_row(self,column):
        return self.empty_spaces[column]

    def get_winner(self):
        status = True
        for col in self.empty_spaces:
            if col < Game.ROW_NUMBER:
                status = False
                break
        if status: return Game.DRAW
        if self.check_winning_move():
            if self.current_player:
                return Game.PLAYER_ONE
            return Game.PLAYER_TWO

        return None
    def check_column(self):
        last_player = int(not self.current_player)
        count = 0
        if self.empty_spaces[self.last_move] < 3:
            for i in range(4):
                if self.board[self.last_move][i + self.empty_spaces[self.last_move]] == last_player:
                    count += 1
            if count == 4: return True
        return False

    def check_row(self):
        last_player = int(not self.current_player)
        count = 0
        for i in range(Game.COL_NUMBER):
            if self.board[i][self.empty_spaces[self.last_move]] == last_player:
                count += 1
            else:
                count = 0
            if count == 4: return True
        return False

    def check_diag(self):
        last_player = int(not self.current_player)
        count = 0
        cell_add_value = self.last_move + self.empty_spaces[self.last_move]

        if (self.last_move + self.empty_spaces[self.last_move] > 2) \
                and (self.last_move + self.empty_spaces[self.last_move] < 9):
            if self.last_move + self.empty_spaces[self.last_move] < 6:
                tup = (cell_add_value,0)
                target = (0,cell_add_value)
            else:
                tup = (Game.ROW_NUMBER-1,cell_add_value-Game.ROW_NUMBER+1 )
                target = (cell_add_value-Game.COL_NUMBER+1,Game.COL_NUMBER-1)
            while tup != target:
                if self.board[tup[1]][tup[0]] == last_player:
                    count += 1
                else:
                    count = 0
                if count == 4 : return True
                tup = (tup[0]-1,tup[1]+1)

        cell_sub_value = self.last_move - self.empty_spaces[self.last_move]
        if cell_sub_value < 4 and cell_sub_value > -3:
            if cell_sub_value > 0 :
                tup = (0, cell_sub_value)
                target = (Game.ROW_NUMBER - cell_sub_value,Game.COL_NUMBER-1 )
            else:
                tup = (cell_sub_value * -1, 0)
                print(cell_sub_value)
                target = (Game.ROW_NUMBER - 1,Game.ROW_NUMBER -1 + cell_sub_value)

            while tup != target:
                if self.board[tup[1]][tup[0]] == last_player:
                    count += 1
                else:
                    count = 0
                if count == 4: return True
                tup = (tup[0] + 1, tup[1] + 1)
            return False

    def check_winning_move(self):
        return  self.check_row() or self.check_column() or self.check_diag()


    def get_player_at(self, row, col):
        if self.board[col][row] == Game.PLAYER_ONE:
            return Game.PLAYER_ONE
        elif self.board[col][row] == Game.PLAYER_TWO:
            return Game.PLAYER_TWO
        return None

    def get_current_player(self):
        if self.current_player:
            return Game.PLAYER_TWO
        return Game.PLAYER_ONE
    def get_board(self):
        return copy.deepcopy(self.board)
    def print_board(self):
        """ prints a board to the screen

        ---  board should be implemented as a dictinary
             that points from a location to a number {(row,col):num}
        """
        for row in range(Game.ROW_NUMBER):
            toPrint = '|'
            for col in range(Game.COL_NUMBER):
                toPrint += '|'+ str(self.board[col][row])
            toPrint += '|'
            print(toPrint)
        print('-------------')