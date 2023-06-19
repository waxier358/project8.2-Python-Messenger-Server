import tkinter
from tkinter import BOTH
from fonts_and_colors import background_color
from frames import ConnectionFrame, ClientsFrame, MessagesFrame
from functionality import Functionality, Connection, Sounds


class ChatServer(tkinter.Tk):
    """ChatServer class creates and controls ChatServer application"""
    def __init__(self):
        super().__init__()

        self.title('Python Messenger Server')
        self.resizable(False, False)
        self.geometry(f'466x{self.winfo_screenheight() - 140}')
        self.iconbitmap('icon/chat_icon.ico')
        self.configure(background=background_color)

        self.connection_frame = ConnectionFrame(self)
        self.connection_frame.pack(fill=BOTH)

        self.clients_frame = ClientsFrame(self)
        self.clients_frame.pack()

        self.messages_frame = MessagesFrame(self)
        self.messages_frame.pack(padx=20, pady=20)

        self.connection = Connection()
        self.functionality = Functionality(self)

        self.sounds = Sounds(self)

        # add functionality on start_button
        self.connection_frame.start_button.configure(command=lambda: self.functionality.start_stop_server(self.
                                                                                                          connection))

    def destroy(self) -> None:
        """action performed when main window is closed
           stop server and destroy main_window
           input: tkinter.Tk
           return: None"""
        self.functionality.stop_server(self.connection)
        tkinter.Tk.destroy(self)
