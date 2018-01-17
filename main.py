import socket
import tkinter as t
import math
from game import Game
from communicator import Communicator
from tkinter.messagebox import showinfo




class GUI:
    """
    Designed to handle the GUI aspects (creating a window, buttons and
    pop-ups. Also initializes the communicator object.
    """
    DRAW_MASSAGE = "It's a draw"
    WIN_MASSAGE = "You Won"
    MESSAGE_DISPLAY_TIMEOUT = 250

    def __init__(self, parent, port, ip=None):
        self.game_obj=Game()
        """
        Initializes the GUI and connects the communicator.
        :param parent: the tkinter root.
        :param ip: the ip to connect to.
        :param port: the port to connect to.
        :param server: true if the communicator is a server, otherwise false.
        """
        
        self._parent = parent


        self.__communicator = Communicator(parent, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)
        #self.__place_widgets()
        self._canvas = t.Canvas(self._parent, width=700, height=600, bg='blue')
        self._canvas.pack()
        self._create_circle()

        self._canvas.bind("<Button-1>", self.callback)


    def popup_showinfo(self,obj):
        showinfo("Window", "Hello World!")


    def _create_circle(self):
        for j in range(6):
            for i in range(7):
                x_place = (100 * i)+50
                y_place = (100 * j)+50
                r = 47.5

                self._canvas.create_oval(x_place - r, y_place - r, x_place + r, y_place + r,fill='white')

    def callback(self, event):

        #print('çlic', event.x,event.y)
        pressedPoint=[event.x,event.y]
        print('column=',math.floor(event.x/100))
        column=math.floor(event.x/100)
        self.game_obj.make_move(column)
        self.color_circle(self.game_obj.get_current_player(),column)
        if self.game_obj.get_winner() == 0 or self.game_obj.get_winner() == 1 or self.game_obj.get_winner() == 2:
            self.popup_showinfo("")
        # return column

    def color_circle(self, player, column):
        x_place = (100*column) + 50

        y_place = (100*self.game_obj.get_empty_row(column)) + 50
        r = 47.5
        if player == 0:
            self._canvas.create_oval(x_place - r, y_place - r, x_place + r, y_place + r, fill='red')
        if player ==1:
            self._canvas.create_oval(x_place - r, y_place - r, x_place + r, y_place + r, fill='yellow')
        pass

#    tk.Canvas.create_circle = _create_circle

    def __handle_message(self, text=None):
        """
        Specifies the event handler for the message getting event in the
        communicator. Prints a message when invoked (and invoked by the
        communicator when a message is received). The message will
        automatically disappear after a fixed interval.
        :param text: the text to be printed.
        :return: None.
        """
        if text:
            self.__label["text"] = text
            self._parent.after(self.MESSAGE_DISPLAY_TIMEOUT,
                               self.__handle_message)
        else:
            self.__label["text"] = ""


if __name__ == '__main__':
    root = t.Tk()

    # Finds out the IP, to be used cross-platform without special issues.
    # (on local machine, could also use "localhost" or "127.0.0.1")
    port = 8000
    server = False
    if server:
        GUI(root, port)
        root.title("Server")
    else:
        GUI(root, port, socket.gethostbyname(socket.gethostname()))
        root.title("Client")
    root.mainloop()
