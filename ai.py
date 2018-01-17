
class AI:

    def find_legal_move(self, g, func, timeout=None):
        possible_moves = g.get_empty_spaces()
        for i in range(len(possible_moves)):
            if possible_moves[i] != 0:
                g.make_move(i)
