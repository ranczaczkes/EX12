from game import Game

class GameRunner:
    def __init__(self,):
        pass

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop,5)

    def _game_loop(self):
        pass

class Screen:
    def __init__(self):
        pass
