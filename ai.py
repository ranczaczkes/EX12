import random
class Ai:

    def __init__(self):
        pass
    def find_legal_move(self, g, func, timeout=None):

        possible_moves = g.get_empty_spaces()
        print("possible moves: ",possible_moves)
        new_list = []
        for i in range(len(possible_moves)):
            print('possible:',possible_moves[i])
            if possible_moves[i] != 0:
                new_list.append(i)

        if len(new_list) != 0:
            i = random.choice(new_list)
            g.make_move(i)
            return
        raise Exception("No more moves can be done, the game is over")

