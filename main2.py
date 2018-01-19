import socket
import tkinter as t
import math
from game import Game
from communicator import Communicator
from tkinter.messagebox import showinfo
import sys
from ai import Ai




class GUI:
    """
    Designed to handle the GUI aspects (creating a window, buttons and
    pop-ups. Also initializes the communicator object.
    """

    MESSAGE_DISPLAY_TIMEOUT = 250

    def __init__(self,root, parent, port, ip=None):
        self.game_obj=Game()
        self._ai_mode = False
        print('parent:',parent)
        print('port:', port)


        """
        Initializes the GUI and connects the communicator.
        :param parent: the tkinter root.
        :param ip: the ip to connect to.
        :param port: the port to connect to.
        :param server: true if the communicator is a server, otherwise false.
        """
        
        self._root = root
        self._parent = parent

        self.__communicator = Communicator(root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)
        self.__place_widgets()
        #self.frame = t.Frame(self._parent, width=800, height=800)

        self._canvas = t.Canvas(root, width=700, height=600, bg='blue')
        self._grid= t.Grid()
        #self.frame.pack()
        self._canvas.pack()
        self._create_circle()

        if parent == 'ai':
            self.ai_obj= Ai()
            self._ai_mode = True
            if (server == True and self.game_obj.get_current_player() == 0) or (
                    server == False and self.game_obj.get_current_player() == 1):
                self.ai_move()
        else:
            self._canvas.bind("<Button-1>", self.callback)






    def __place_widgets(self):
        pass

    def popup_showinfo(self,obj):
        showinfo("Window", "The winner is: " + str(obj))


    def _create_circle(self):
        board = self.game_obj.get_board()

        for j in range(6):
            for i in range(7):
                x_place = (100 * i)+50
                y_place = (100 * j)+50
                r = 47.5
                color = "white"
                if board[i][j] == "0": color = "red"
                if board[i][j] == "1": color = "yellow"
                self._canvas.create_oval(x_place - r, y_place - r, x_place + r, y_place + r,fill=color)



    def callback(self, event):

        print('column=',math.floor(event.x/100))
        column=math.floor(event.x/100)
        if (server == True and self.game_obj.get_current_player() == 0) \
                or (server == False and self.game_obj.get_current_player() == 1):
            self.game_obj.make_move(column)
            self.color_circle(self.game_obj.get_current_player(), column)
            message = str(column)

            is_winner =self.game_obj.get_winner()

            if  is_winner == 0 or is_winner == 1 or is_winner == 2:
                message += str(is_winner)
                self.popup_showinfo(is_winner)

            self.__communicator.send_message(message)
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
            if len(text) > 1:
                self.popup_showinfo(text[1])
            else:
                column=int(text[0])
                print("The column i got is:",column)
                self.game_obj.make_move(column)
                self.color_circle(self.game_obj.get_current_player(), column)


                if self._ai_mode:
                    self.ai_move()

                self._root.after(self.MESSAGE_DISPLAY_TIMEOUT,
                                 self.__handle_message)
       # else:
            #self.__label["text"] = ""
        pass
    def ai_move(self):
        self.ai_obj.find_legal_move(self.game_obj, self.ai_move)
        column =  self.game_obj.get_last_move()
        self.color_circle(self.game_obj.get_current_player(),column)

        message = str(column)

        is_winner =self.game_obj.get_winner()
        print("who is the winner: ",self.game_obj.get_winner())
        if  is_winner == 0 or is_winner == 1 or is_winner == 2:
            message += str(is_winner)
            self.popup_showinfo(is_winner)

        self.__communicator.send_message(message)


if __name__ == '__main__':
    root = t.Tk()
    root.title(" 4 in Row - V 1.0 -- Arkadi & Ran")
    server = False
    if len(sys.argv) == 3:
        server = True

    # Finds out the IP, to be used cross-platform without special issues.
    # (on local machine, could also use "localhost" or "127.0.0.1")
    port = 8000

    if server:
         GUI(root,sys.argv[1],sys.argv[2])
         root.title("Server")
    else:
         GUI(root,sys.argv[1] ,sys.argv[2], sys.argv[3])
         root.title("Client")

    root.mainloop()
