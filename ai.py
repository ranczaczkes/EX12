
class Ai:
    def __init__(self):
        pass
    def find_legal_move(self, g, func, timeout=None):

        possible_moves = g.get_empty_spaces()
        print("possible moves: ",possible_moves)
        for i in range(len(possible_moves)):
            print('possible:',possible_moves[i])
            if possible_moves[i] != 0:
                g.make_move(i)
                #func((i*100,0))
                return
        raise Exception("No more moves can be done, the game is over")

